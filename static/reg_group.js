function applyGroupFilters() {
  const formEducation = document.getElementById("formEducation").value;
  const directStudy = document.getElementById("directStudy").value;
  const yearStudy = document.getElementById("yearStudy").value;
  if (!formEducation && !directStudy && !yearStudy) {
    return;
  }
  getData(formEducation, directStudy, yearStudy)
}

function dropGroupFilters() {
  getData(null, null, null)
}

function getData(formEducation, directStudy, yearStudy) {
  $.ajax({
    type: "POST",
    url: "/admin/groups",
    dataSrc: "data",
    data: { formEducation, directStudy, yearStudy },
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
