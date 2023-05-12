function applyMembersFilters() {
  const projectFioFilter = document.getElementById("projectFioFilter").value;
  const projectRoleFilter = document.getElementById("projectRoleFilter").value;
  const projectNaprFilter = document.getElementById("projectNaprFilter").value;

  if (!projectFioFilter && !projectRoleFilter && !projectNaprFilter) {
    return;
  }
  getDataMembers(projectFioFilter, projectRoleFilter, projectNaprFilter);
}

function dropMembersFilter() {
  getDataMembers(null, null, null);
}

function getDataMembers(
  projectFioFilter,
  projectRoleFilter,
  projectNaprFilter
) {
  const url = window.location.pathname.split("/")[1];
  $.ajax({
    type: "POST",
    url: "/" + url + "/members",
    dataSrc: "data",
    data: { projectFioFilter, projectRoleFilter, projectNaprFilter },
    success: function (data) {
      const accordion = document.getElementById("membersAccordion");
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

function getCompetitionsSpec(id, operation) {
  $.ajax({
    type: "GET",
    dataSrc: "data",
    data: { id },
    url: "/getCompetitionsSpec",
    success: function (data) {
      const checkboxes = document.getElementById(operation + "Wrapper");
      const elements = document.querySelectorAll(
        "#" + operation + 'Wrapper input[type="checkbox"]:checked'
      );
      let checkboxData = "";
      for (el of elements) {
        checkboxData += `<div class="form-check">${el.outerHTML.replace(
          ">",
          " checked>"
        )}${el.nextElementSibling.outerHTML}</div>`;
      }
      for (el of data) {
        if (
          !elements.length ||
          !document.getElementById(`add_spec_${el[0]}_${id}`)
        )
          checkboxData += `<div class="form-check">
          <input class="form-check-input" name="comp" type="checkbox" value="${el[0]}"
            id="add_spec_${el[0]}_${id}">
          <label class="form-check-label" for="add_spec_${el[0]}_${id}">
            ${el[1]} - ${el[2]}
          </label>
          </div>`;
      }
      if (checkboxData == "") checkboxData = "<p>Данных не найдено</p>";
      checkboxes.innerHTML = checkboxData;
    },
  });
}

function applyRolesFilters() {
  const projectFilter = document.getElementById("projectFilter").value;
  const opopFilter = document.getElementById("opopFilter").value;
  const projectRoleFilter = document.getElementById("projectRoleFilter").value;

  if (!projectFilter && !projectRoleFilter && !opopFilter) {
    return;
  }
  getDataRoles(projectFilter, projectRoleFilter, opopFilter);
}

function dropRolesFilter() {
  getDataRoles(null, null, null);
}

function getDataRoles(
  projectFilter, projectRoleFilter, opopFilter
) {
  const url = window.location.pathname.split("/")[1];
  $.ajax({
    type: "POST",
    url: "/" + url + "/roles",
    dataSrc: "data",
    data: { projectFilter, projectRoleFilter, opopFilter },
    success: function (data) {
      const accordion = document.getElementById("membersAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}
