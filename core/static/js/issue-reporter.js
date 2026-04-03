(function() {
  const GITHUB_REPO = 'miratcan/kaydet.link';
  let active = false;
  let selectedEl = null;
  let hoveredEl = null;

  function getXPath(el) {
    if (!el || el === document.body) return '/html/body';
    const parts = [];
    while (el && el.nodeType === 1) {
      let idx = 1;
      let sib = el.previousElementSibling;
      while (sib) {
        if (sib.tagName === el.tagName) idx++;
        sib = sib.previousElementSibling;
      }
      const tag = el.tagName.toLowerCase();
      parts.unshift(tag + '[' + idx + ']');
      el = el.parentElement;
    }
    return '/' + parts.join('/');
  }

  function isReporterUI(el) {
    return el && (el.closest('#issue-reporter-modal') || el.closest('#issue-reporter-btn'));
  }

  function onMouseOver(e) {
    if (isReporterUI(e.target)) return;
    if (hoveredEl && hoveredEl !== selectedEl) {
      hoveredEl.style.outline = hoveredEl._origOutline || '';
    }
    hoveredEl = e.target;
    if (hoveredEl !== selectedEl) {
      hoveredEl._origOutline = hoveredEl.style.outline;
      hoveredEl.style.outline = '2px solid red';
    }
  }

  function onMouseOut(e) {
    if (isReporterUI(e.target)) return;
    if (hoveredEl && hoveredEl !== selectedEl) {
      hoveredEl.style.outline = hoveredEl._origOutline || '';
    }
  }

  function onClick(e) {
    if (isReporterUI(e.target)) return;
    e.preventDefault();
    e.stopPropagation();

    if (selectedEl) {
      selectedEl.style.outline = selectedEl._origOutline || '';
    }

    selectedEl = e.target;
    selectedEl._origOutline = selectedEl._origOutline || '';
    selectedEl.style.outline = '3px solid #22c55e';

    showModal();
  }

  function createModal() {
    const modal = document.createElement('div');
    modal.id = 'issue-reporter-modal';
    modal.style.display = 'none';

    const backdrop = document.createElement('div');
    backdrop.className = 'ir-backdrop';
    modal.appendChild(backdrop);

    const dialog = document.createElement('div');
    dialog.className = 'ir-dialog';

    const h3 = document.createElement('h3');
    h3.textContent = 'Issue Bildir';
    dialog.appendChild(h3);

    const titleLabel = document.createElement('label');
    titleLabel.textContent = 'Başlık';
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.id = 'ir-title';
    titleInput.placeholder = 'Kısa açıklama';
    titleLabel.appendChild(titleInput);
    dialog.appendChild(titleLabel);

    const bodyLabel = document.createElement('label');
    bodyLabel.textContent = 'Açıklama';
    const bodyTextarea = document.createElement('textarea');
    bodyTextarea.id = 'ir-body';
    bodyTextarea.rows = 4;
    bodyTextarea.placeholder = 'Detaylı açıklama (opsiyonel)';
    bodyLabel.appendChild(bodyTextarea);
    dialog.appendChild(bodyLabel);

    const info = document.createElement('div');
    info.className = 'ir-info';
    const small = document.createElement('small');
    small.textContent = 'Seçilen eleman: ';
    const code = document.createElement('code');
    code.id = 'ir-xpath';
    small.appendChild(code);
    info.appendChild(small);
    dialog.appendChild(info);

    const actions = document.createElement('div');
    actions.className = 'ir-actions';

    const cancelBtn = document.createElement('button');
    cancelBtn.type = 'button';
    cancelBtn.id = 'ir-cancel';
    cancelBtn.textContent = 'İptal';
    actions.appendChild(cancelBtn);

    const submitBtn = document.createElement('button');
    submitBtn.type = 'button';
    submitBtn.id = 'ir-submit';
    submitBtn.textContent = "GitHub'da Aç";
    actions.appendChild(submitBtn);

    dialog.appendChild(actions);
    modal.appendChild(dialog);
    document.body.appendChild(modal);

    cancelBtn.addEventListener('click', function() {
      closeModal();
      deactivate();
    });

    submitBtn.addEventListener('click', function() {
      submitIssue();
    });

    backdrop.addEventListener('click', function() {
      closeModal();
      deactivate();
    });

    return modal;
  }

  function showModal() {
    let modal = document.getElementById('issue-reporter-modal');
    if (!modal) {
      modal = createModal();
    }

    const xpath = getXPath(selectedEl);
    document.getElementById('ir-xpath').textContent = xpath;
    modal.style.display = 'flex';
    document.getElementById('ir-title').focus();
  }

  function closeModal() {
    const modal = document.getElementById('issue-reporter-modal');
    if (modal) modal.style.display = 'none';
  }

  function submitIssue() {
    const title = document.getElementById('ir-title').value.trim();
    if (!title) {
      document.getElementById('ir-title').style.borderColor = 'red';
      return;
    }

    const description = document.getElementById('ir-body').value.trim();
    const xpath = getXPath(selectedEl);
    const pageUrl = window.location.href;
    const pageTitle = document.title;
    const elText = selectedEl.textContent.trim().substring(0, 100);

    const body = [
      '## Sayfa',
      '- **URL:** ' + pageUrl,
      '- **Başlık:** ' + pageTitle,
      '',
      '## Seçilen Eleman',
      '- **XPath:** `' + xpath + '`',
      '- **İçerik:** ' + (elText ? '"' + elText + '"' : '(boş)'),
      '',
      '## Açıklama',
      description || '(açıklama girilmedi)',
    ].join('\n');

    const url = 'https://github.com/' + GITHUB_REPO + '/issues/new?'
      + 'title=' + encodeURIComponent(title)
      + '&body=' + encodeURIComponent(body)
      + '&labels=' + encodeURIComponent('bug');

    window.open(url, '_blank');
    closeModal();
    deactivate();
  }

  function activate() {
    active = true;
    document.body.style.cursor = 'crosshair';
    document.addEventListener('mouseover', onMouseOver, true);
    document.addEventListener('mouseout', onMouseOut, true);
    document.addEventListener('click', onClick, true);
    document.addEventListener('keydown', onKeyDown, true);
  }

  function deactivate() {
    active = false;
    document.body.style.cursor = '';
    document.removeEventListener('mouseover', onMouseOver, true);
    document.removeEventListener('mouseout', onMouseOut, true);
    document.removeEventListener('click', onClick, true);
    document.removeEventListener('keydown', onKeyDown, true);
    if (hoveredEl) {
      hoveredEl.style.outline = hoveredEl._origOutline || '';
      hoveredEl = null;
    }
    if (selectedEl) {
      selectedEl.style.outline = selectedEl._origOutline || '';
      selectedEl = null;
    }
  }

  function onKeyDown(e) {
    if (e.key === 'Escape') {
      closeModal();
      deactivate();
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('issue-reporter-btn');
    if (!btn) return;
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      if (active) {
        deactivate();
      } else {
        activate();
      }
    });
  });
})();
