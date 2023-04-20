function applyorgFilters() {
  const fioFilters = document.getElementById("fioFilter").value;
  const orgFilters = document.getElementById("orgFilter").value;
  const yuradressFilters = document.getElementById("yuradressFilter").value;
  if (!fioFilters && !orgFilters && !yuradressFilters) {
    return;
  }
  getDataOrg(fioFilters, orgFilters, yuradressFilters);
}

function droporgFilters() {
  getDataOrg(null, null, null);
}

function getDataOrg(fioFilters, orgFilters, yuradressFilters) {
  $.ajax({
    type: "POST",
    url: "/admin/organization",
    dataSrc: "data",
    data: { fioFilters, orgFilters, yuradressFilters },
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
      table.className = "collapse show";
    },
    error: function (err) {
      console.log(err);
    },
  });
}
