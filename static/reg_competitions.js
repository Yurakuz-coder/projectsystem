function applySpec() {
  const spec = document.getElementById("spec").value;
  console.log(spec);
  if (!spec) {
    return;
  }
  getDataComp(spec);
}

function getDataComp(spec) {
  $.ajax({
    type: "POST",
    url: "/admin/competitions",
    dataSrc: "data",
    data: { spec },
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
