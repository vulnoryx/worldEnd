setInterval(timerUpdate, 1000);

function timerUpdate() {
  const d = new Date();

  // update time
  document.getElementById("time").innerHTML = d.toLocaleTimeString('es-ES', {
    hour12: false,
  });

  // update date
  const weekday = d.toLocaleDateString('en-GB', { weekday: 'long' });
  const day = d.getDate();
  const month = d.toLocaleDateString('en-GB', { month: 'long' });
  const year = d.getFullYear();
  
  const formattedDate = `${weekday}, ${day} ${month} ${year}`;

  document.getElementById("date").innerHTML = formattedDate;
}