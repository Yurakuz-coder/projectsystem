function applyStudentWorksFilter() {
  const projectFilter = document.getElementById("projectFilter").value;
  const stageFilter = document.getElementById("stageFilter").value;
  if (!projectFilter && !stageFilter) {
    return;
  }
  getDataStudentsWorks(stageFilter, projectFilter);
}

function dropStudentsWorksFilters() {
  getDataStudentsWorks(null, null);
}

function getDataStudentsWorks(stageFilter, projectFilter) {
  $.ajax({
    type: "POST",
    url: "/student/works",
    dataSrc: "data",
    data: { stageFilter, projectFilter },
    success: function (data) {
      const table = document.getElementById("projectsAccordion");
      table.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function applyStudentsFilters() {
  const fio = document.getElementById("fio").value;
  const grname = document.getElementById("grname").value;
  if (!fio && !grname) {
    return;
  }
  getDataStudents(fio, grname);
}

function dropStudentsFilters() {
  getDataStudents(null, null);
}

function getDataStudents(fio, grname) {
  $.ajax({
    type: "POST",
    url: "/admin/students",
    dataSrc: "data",
    data: { fio, grname },
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function uploadCsvStudFile() {
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
    url: "/admin/csvStud",
    success: function () {
      button.innerHTML = "Файл загружен!";
    },
    error: function (data) {
      button.innerHTML = "Файл не загружен! - " + data?.responseText;
    },
  });
}

function getStudentsGroup(idGroup, op) {
  $.ajax({
    type: "GET",
    url: "/admin/getStudentsGroup",
    data: { idGroup },
    success: function (data) {
      const select = document.getElementById(op + "Students");
      const button = document.getElementById(op + "StudentButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Студенты не найдены", 0));
        select.disabled = true;
        button.disabled = true
        return;
      }
      select.disabled = false;
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(
            `${item.FullName} #${item.studentsStudbook}`,
            item.IDstudents
          )
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}
