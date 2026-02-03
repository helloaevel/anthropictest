(function() {
  var monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var current = new Date();
  var gridEl = document.getElementById('cal-grid');
  var titleEl = document.getElementById('cal-title');
  var eventsListEl = document.getElementById('events-list');

  function api(method, path, body) {
    var opts = { method: method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    return fetch(path, opts).then(function(r) { return r.json(); });
  }

  function loadEvents() {
    return api('GET', '/api/events').then(function(data) { return data.events || []; });
  }

  function renderCalendar() {
    if (!gridEl || !titleEl) return;
    var y = current.getFullYear();
    var m = current.getMonth();
    titleEl.textContent = monthNames[m] + ' ' + y;
    var first = new Date(y, m, 1);
    var last = new Date(y, m + 1, 0);
    var startDay = first.getDay();
    var daysInMonth = last.getDate();
    loadEvents().then(function(events) {
      var eventDates = {};
      events.forEach(function(ev) {
        var d = ev.date;
        if (d) eventDates[d] = (eventDates[d] || 0) + 1;
      });
      var html = '';
      var dayNames = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
      dayNames.forEach(function(d) { html += '<div class="cal-cell head">' + d + '</div>'; });
      var pad = startDay;
      var prevMonth = new Date(y, m, 0);
      var prevDays = prevMonth.getDate();
      for (var i = 0; i < pad; i++) {
        html += '<div class="cal-cell other">' + (prevDays - pad + i + 1) + '</div>';
      }
      for (var d = 1; d <= daysInMonth; d++) {
        var dateStr = y + '-' + String(m + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0');
        var cls = 'cal-cell' + (eventDates[dateStr] ? ' has-event' : '');
        html += '<div class="cal-cell ' + (eventDates[dateStr] ? 'has-event' : '') + '" data-date="' + dateStr + '">' + d + '</div>';
      }
      var total = pad + daysInMonth;
      var rest = total % 7 ? 7 - (total % 7) : 0;
      for (var j = 0; j < rest; j++) {
        html += '<div class="cal-cell other">' + (j + 1) + '</div>';
      }
      gridEl.innerHTML = html;
      renderEventsList(events, y, m);
    });
  }

  function renderEventsList(events, y, m) {
    if (!eventsListEl) return;
    var monthStr = String(m + 1).padStart(2, '0');
    var inMonth = events.filter(function(e) {
      return e.date && e.date.startsWith(y + '-' + monthStr);
    }).sort(function(a, b) { return (a.date || '').localeCompare(b.date || ''); });
    eventsListEl.innerHTML = inMonth.length ? inMonth.map(function(ev) {
      return '<li><span>' + (ev.date || '') + ' — ' + (ev.title || '').replace(/</g, '&lt;') + '</span><button type="button" class="btn btn-small btn-danger" data-id="' + (ev.id || '') + '" aria-label="Delete event">Delete</button></li>';
    }).join('') : '<li class="empty-state"><p class="empty-state__title">No events this month</p><p>Add one using the form above.</p></li>';
    eventsListEl.querySelectorAll('.btn-danger').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var id = btn.getAttribute('data-id');
        if (!id) return;
        var label = (btn.closest('li') && btn.closest('li').querySelector('span') && btn.closest('li').querySelector('span').textContent) || 'this event';
        if (typeof Aevel !== 'undefined' && Aevel.confirm) {
          Aevel.confirm({ title: 'Delete event', body: 'Delete “‘ + label.substring(0, 50) + (label.length > 50 ? '…”' : '”') + '?', confirmLabel: 'Delete', cancelLabel: 'Cancel', danger: true }, function() {
            api('DELETE', '/api/events/' + id).then(function() { renderCalendar(); if (Aevel.toast) Aevel.toast('Event deleted', 'success'); });
          });
        } else {
          api('DELETE', '/api/events/' + id).then(function() { renderCalendar(); });
        }
      });
    });
  }

  var prevBtn = document.getElementById('cal-prev');
  var nextBtn = document.getElementById('cal-next');
  if (prevBtn) prevBtn.addEventListener('click', function() { current.setMonth(current.getMonth() - 1); renderCalendar(); });
  if (nextBtn) nextBtn.addEventListener('click', function() { current.setMonth(current.getMonth() + 1); renderCalendar(); });

  var calForm = document.getElementById('cal-form');
  if (calForm) {
    calForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var dateEl = document.getElementById('cal-date');
      var titleEl = document.getElementById('cal-title-input');
      var date = dateEl && dateEl.value;
      var title = titleEl && titleEl.value && titleEl.value.trim();
      if (!date || !title) return;
      api('POST', '/api/events', { date: date, title: title }).then(function() {
        if (titleEl) titleEl.value = '';
        if (dateEl) dateEl.value = '';
        renderCalendar();
        if (typeof Aevel !== 'undefined' && Aevel.toast) Aevel.toast('Event added', 'success');
      });
    });
  }

  renderCalendar();
})();
