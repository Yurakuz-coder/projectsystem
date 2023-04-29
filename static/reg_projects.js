function applyProjectFilters() {
  const projectFilter = document.getElementById("projectFilter").value;
  const stadiaFilter = document.getElementById("stadiaFilter").value;

  if (!projectFilter && !stadiaFilter) {
    return;
  }
  getDataProject(projectFilter, stadiaFilter);
}

function dropProjectFilter() {
  getDataProject(null, null);
}

function getDataProject(projectFilter, stadiaFilter) {
  const url = window.location.pathname.split('/')[1]
  $.ajax({
    type: "POST",
    url: "/" + url + "/projects",
    dataSrc: "data",
    data: { projectFilter, stadiaFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function uploadPassportFile(id) {
  const formData = new FormData();
  const button = document.getElementById("button-upload" + id);
  const file = document.getElementById("input-upload" + id).files[0];
  if (!file) return;
  formData.append("file", file);
  formData.append("passport_id", id);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/uploadPassportSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deletePassportFile(id) {
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idPassport: id },
    url: "/deletePassportSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
  });
}

function checkStadia(id) {
  $.ajax({
    type: "GET",
    dataSrc: "data",
    data: { idProject: id },
    url: "/checkStadia",
    success: function (data) {
      const select = document.getElementById("stadia");
      select.innerHTML = "";
      if (data.IDstadiaofpr) {
        select.disabled = true;
        select.add(
          new Option(
            `${data.stadiaofprName}`,
            ''
          )
        )
      }
      else {
        select.disabled = false;
        data.map(item => {
          select.add(
            new Option(
              `${item.stadiaofprName}`,
              item.IDstadiaofpr
            )
          )
        })
      }
    },
    error: function (data) {
      console.log(data)
    }
  });
}
