/* FLOW EDITOR — JavaScript utilitário */

function showAlert(message, type = 'info', duration = 3500) {
  let el = document.getElementById('flash-alert');
  if (!el) {
    el = document.createElement('div');
    el.id = 'flash-alert';
    document.body.appendChild(el);
  }
  el.className = `alert alert-${type}`;
  el.textContent = message;
  el.style.display = 'block';
  clearTimeout(window._alertTimeout);
  window._alertTimeout = setTimeout(() => { el.style.display = 'none'; }, duration);
}

// Formata moeda BRL
function formatBRL(value) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value || 0);
}

// Confirma ação destrutiva
function confirmAction(msg) {
  return confirm(msg || 'Tem certeza?');
}

// Feedback de loading em botão
function setLoading(btn, loading, originalText) {
  if (loading) {
    btn.disabled = true;
    btn._orig = btn.textContent;
    btn.textContent = '⏳ Aguarde...';
  } else {
    btn.disabled = false;
    btn.textContent = originalText || btn._orig || 'OK';
  }
}

// Formata data pt-BR
function formatDate(isoString) {
  if (!isoString) return '—';
  return new Date(isoString).toLocaleDateString('pt-BR');
}

// Sanitiza texto para uso seguro
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Auto-resize textarea
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('textarea').forEach(ta => {
    ta.addEventListener('input', function() {
      if (this.scrollHeight > this.clientHeight && this.rows < 30) {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
      }
    });
  });

  // Destaca link ativo na sidebar baseado na URL
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
});

// Debounce para auto-save
function debounce(fn, delay) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), delay);
  };
}
