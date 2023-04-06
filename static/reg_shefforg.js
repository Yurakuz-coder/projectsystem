function applyFilters() {
  const fioFilter = document.getElementById("fioFilter").value;
  const orgFilter = document.getElementById("orgFilter").value;
  if (!fioFilter && !orgFilter) {
    return;
  }
  getData(fioFilter, orgFilter)
}

function dropFilter() {
  getData(null, null)
}

function getData(fioFilter, orgFilter) {
  $.ajax({
    type: "POST",
    url: "/admin/reg_shefforg",
    dataSrc: "data",
    data: { fioFilter, orgFilter },
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
