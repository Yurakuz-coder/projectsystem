function applyorgFilters(page) {
  const fioFilters = document.getElementById("fioFilter").value;
  const orgFilters = document.getElementById("orgFilter").value;
  const yuradressFilters = document.getElementById("yuradressFilter").value;
  if (page == undefined && !fioFilters && !orgFilters && !yuradressFilters) {
    return;
  }
  getDataOrg(page, fioFilters, orgFilters, yuradressFilters);
}

function droporgFilters() {
  const fioFilters = document.getElementById("fioFilter");
  const orgFilters = document.getElementById("orgFilter");
  fioFilters && (fioFilters.value = "")
  orgFilters && (orgFilters.value = "")
  getDataOrg(null, null, null, null);
}

function getDataOrg(page, fioFilters, orgFilters, yuradressFilters) {
  $.ajax({
    type: "POST",
    url: "/admin/organization",
    dataSrc: "data",
    data: { page, fioFilters, orgFilters, yuradressFilters },
    success: function (data) {
      const resultTable = document.getElementById("resultTable");
      resultTable.innerHTML = data;
      const table = document.getElementById("collapseTableBody");
      table.className = "collapse show";
    },
    error: function (err) {
      console.log(err);
    },
  });
}
