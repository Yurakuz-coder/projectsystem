function applyGroupFilters() {
  const formEducation = document.getElementById("formEducation").value;
  const directStudy = document.getElementById("directStudy").value;
  const yearStudy = document.getElementById("yearStudy").value;
  const nameGroup = document.getElementById("nameGroup").value;
  if (!formEducation && !directStudy && !yearStudy && !nameGroup) {
    return;
  }
  getDataGroup(formEducation, directStudy, yearStudy, nameGroup);
}

function dropGroupFilters() {
  getDataGroup(null, null, null, null);
}

function getDataGroup(formEducation, directStudy, yearStudy, nameGroup) {
  $.ajax({
    type: "POST",
    url: "/admin/groups",
    dataSrc: "data",
    data: { formEducation, directStudy, yearStudy, nameGroup },
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

function uploadCsvGroupFile() {
  const formData = new FormData();
  const button = document.getElementById("button-upload-csv");
  const file = document.getElementById("input-upload-csv").files[0];
  if (!file) return;
  formData.append("file", file);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/admin/csvGroup",
    success: function () {
      button.innerHTML = "Файл загружен!";
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}
