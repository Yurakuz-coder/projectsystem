function applyorgFilters() {
  const fioFilters = document.getElementById("fioFilters").value;
  const orgFilters = document.getElementById("orgFilters").value;
  const yuradressFilters = document.getElementById("yuradressFilters").value;
  if (!fioFilters && !orgFilters && !yuradressFilters) {
    return;
  }
  getData(fioFilters, orgFilters, yuradressFilters)
}

function droporgFilters() {
  getData(null, null, null)
}

function getData(fioFilters, orgFilters, yuradressFilters) {
  $.ajax({
    type: "POST",
    url: "/admin//admin/organization",
    dataSrc: "data",
    data: { fioFilters, orgFilters, yuradressFilters },
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