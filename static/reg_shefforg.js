function applyFilters() {
  const fioFilter = document.getElementById("fioFilter").value;
  const orgFilter = document.getElementById("orgFilter").value;
  if (!fioFilter && !orgFilter) {
    return;
  }

  $.ajax({
    type: "POST",
    url: "/admin/reg_shefforg",
    dataType: "json",
    dataSrc: "data",
    data: { fioFilter, orgFilter },
    success: function (data) {
      document.getElementById("collapseTableBody").innerHTML =
        data.responseText;
    },
    error: function (err) {
      document.getElementById("collapseTableBody").innerHTML = err.responseText;
    },
  });
}
