(function() {
  function api(method, path, body) {
    var opts = { method: method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    return fetch(path, opts).then(function(r) { return r.json(); });
  }

  function loadTasks() {
    return api('GET', '/api/tasks').then(function(data) { return data.tasks || []; });
  }

  function render(tasks) {
    var list = document.getElementById('task-list');
    if (!list) return;
    list.innerHTML = tasks.length ? tasks.map(function(t) {
      return '<li class="task-item ' + (t.done ? 'done' : '') + '" data-id="' + (t.id || '') + '">' +
        '<input type="checkbox" class="task-done" ' + (t.done ? 'checked' : '') + ' aria-label="Mark done">' +
        '<span class="task-text">' + (t.text || '').replace(/</g, '&lt;') + '</span>' +
        '<div class="task-actions"><button type="button" class="btn btn-small btn-danger task-delete" aria-label="Delete task">Delete</button></div></li>';
    }).join('') : '<li class="empty-state"><p class="empty-state__title">No tasks yet</p><p>Add one above to get started.</p></li>';
    list.querySelectorAll('.task-done').forEach(function(cb) {
      cb.addEventListener('change', function() {
        var id = cb.closest('.task-item').getAttribute('data-id');
        if (!id) return;
        var item = tasks.find(function(t) { return String(t.id) === id; });
        api('PATCH', '/api/tasks/' + id, { done: !item.done }).then(function() { loadTasks().then(render); });
      });
    });
    list.querySelectorAll('.task-delete').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var row = btn.closest('.task-item');
        var id = row && row.getAttribute('data-id');
        if (!id) return;
        var text = (row.querySelector('.task-text') && row.querySelector('.task-text').textContent) || 'this task';
        if (typeof Aevel !== 'undefined' && Aevel.confirm) {
          Aevel.confirm({ title: 'Delete task', body: 'Delete “‘ + text.substring(0, 40) + (text.length > 40 ? '…”' : '”') + '? This cannot be undone.', confirmLabel: 'Delete', cancelLabel: 'Cancel', danger: true }, function() {
            api('DELETE', '/api/tasks/' + id).then(function() { loadTasks().then(render); if (Aevel.toast) Aevel.toast('Task deleted', 'success'); });
          });
        } else {
          api('DELETE', '/api/tasks/' + id).then(function() { loadTasks().then(render); });
        }
      });
    });
  }

  var form = document.getElementById('task-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var input = document.getElementById('task-input');
      var text = (input && input.value || '').trim();
      if (!text) return;
      api('POST', '/api/tasks', { text: text }).then(function() {
        input.value = '';
        loadTasks().then(render);
        if (typeof Aevel !== 'undefined' && Aevel.toast) Aevel.toast('Task added', 'success');
      });
    });
  }

  loadTasks().then(render);
})();
