function applySpecFilters() {
  const shifrFilters = document.getElementById("shifrFilter").value;
  const naprFilters = document.getElementById("napravFilter").value;
  if (!shifrFilters && !naprFilters ) {
    return;
  }
  getData(shifrFilters, naprFilters)
}


function dropSpecFilters() {
  getData(null, null)
}


function getData(shifrFilters, naprFilters) {
  $.ajax({
    type: "POST",
    url: "/admin/specializations",
    dataSrc: "data",
    data: { shifrFilters, naprFilters },
    success: function (data) {
      const table = document.getElementById("collapseTableBody")
      table.innerHTML = data;
      table.className = 'collapse show'
    },
    error: function (err) {
      console.log(err)
    },
  });
}