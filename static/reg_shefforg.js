function applyFilters() {
  const fioFilter = document.getElementById('fioFilter')
  const orgFilter = document.getElementById('orgFilter')
  if (!fioFilter.value || orgFilter.value) {
    return
  }

  $.ajax({
    type: "POST",
    url: "/admin/reg_shefforg",
    dataType: "json",
    dataSrc: "data",
    data: { fioFilter: fioFilter.value, orgFilter: orgFilter.value },
    success: function (data) {
      console.log(1)
    },
    error: function (err) {
      console.log("error");
    },
  });

}
