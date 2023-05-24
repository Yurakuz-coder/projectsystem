function applyStudentWorksFilter(page) {
  const projectFilter = document.getElementById("projectFilter")?.value;
  const stageFilter = document.getElementById("stageFilter")?.value;
  const inicFilter = document.getElementById("inicFilter")?.value;
  const sheffProjFilter = document.getElementById("sheffProjFilter")?.value;
  const roleFilter = document.getElementById("roleFilter")?.value;

  if (page == undefined && !projectFilter && !stageFilter && !inicFilter && !sheffProjFilter && !roleFilter) {
    return;
  }
  getDataStudentsWorks(page, sheffProjFilter, roleFilter, inicFilter, stageFilter, projectFilter);
}

function dropStudentsWorksFilters() {
  const projectFilter = document.getElementById("projectFilter");
  const stageFilter = document.getElementById("stageFilter");
  const inicFilter = document.getElementById("inicFilter");
  const sheffProjFilter = document.getElementById("sheffProjFilter");
  const roleFilter = document.getElementById("roleFilter");
  projectFilter && (projectFilter.value = "")
  stageFilter && (stageFilter.value = "")
  inicFilter && (inicFilter.value = "")
  sheffProjFilter && (sheffProjFilter.value = "")
  roleFilter && (roleFilter.value = "")
  getDataStudentsWorks(null, null, null, null, null, null);
}

function getDataStudentsWorks(page, sheffProjFilter, roleFilter, inicFilter, stageFilter, projectFilter) {
  $.ajax({
    type: "POST",
    url: "/student/works",
    dataSrc: "data",
    data: { page, sheffProjFilter, roleFilter, inicFilter, stageFilter, projectFilter },
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
  const fio = document.getElementById("fio")?.value;
  const grname = document.getElementById("grname")?.value;
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

function applyTicketFilters() {
  const roleFilter = document.getElementById("roleFilter")?.value;
  const projectNameFilter = document.getElementById("projectNameFilter")?.value;
  const statusFilter = document.getElementById("statusFilter")?.value;

  if (!statusFilter && !projectNameFilter && !roleFilter) {
    return;
  }
  getDataStudentsTicket(statusFilter, roleFilter, projectNameFilter);
}

function dropTicketFilters() {
  getDataStudentsTicket(null, null, null);
}

function getDataStudentsTicket(statusFilter, roleFilter, projectNameFilter) {
  $.ajax({
    type: "POST",
    url: "/student/tickets",
    dataSrc: "data",
    data: { statusFilter, roleFilter, projectNameFilter },
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}
