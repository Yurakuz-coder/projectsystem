function applyFilters(page) {
  const fioFilter = document.getElementById("fioFilter")?.value;
  const orgFilter = document.getElementById("orgFilter")?.value;
  if (page == undefined && !fioFilter && !orgFilter) {
    return;
  }
  getDataSheffOrg(page, fioFilter, orgFilter);
}

function dropFilter() {
  const fioFilter = document.getElementById("fioFilter");
  const orgFilter = document.getElementById("orgFilter");
  fioFilter && (fioFilter.value = "")
  orgFilter && (orgFilter.value = "")
  getDataSheffOrg(null, null, null);
}

function getDataSheffOrg(page, fioFilter, orgFilter) {
  $.ajax({
    type: "POST",
    url: "/admin/reg_shefforg",
    dataSrc: "data",
    data: { page, fioFilter, orgFilter },
    success: function (data) {
      const result = document.getElementById("resultTable");
      result.innerHTML = data;
      const table = document.getElementById("collapseTableBody");
      table.className = "collapse show";
    },
    error: function (err) {
      console.log(err);
    },
  });
}
