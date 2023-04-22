function applyCafedraFilters() {
  const cafedraFIO = document.getElementById("cafedraFIO").value;
  const cafedraPos = document.getElementById("cafedraPos").value;
  if (!cafedraFIO && !cafedraPos) {
    return;
  }
  getData(cafedraFIO, cafedraPos);
}

function dropCafedraFilters() {
  getData(null, null);
}

function getData(cafedraFIO, cafedraPos) {
  $.ajax({
    type: "POST",
    url: "/admin/cafedra",
    dataSrc: "data",
    data: { cafedraFIO, cafedraPos },
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