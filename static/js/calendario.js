// static/js/calendario.js
document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  // pega o JSON injetado no template (type="application/json")
  var events = [];
  var eventsScript = document.getElementById('events-data');
  if (eventsScript) {
    try {
      events = JSON.parse(eventsScript.textContent || '[]');
    } catch (err) {
      console.error('Erro ao parsear events JSON:', err, eventsScript.textContent);
      events = [];
    }
  }

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'pt-br',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    events: events
  });

  calendar.render();
});
