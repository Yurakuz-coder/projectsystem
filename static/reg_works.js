function applyWorksFilters() {
  const dateContractFilter =
    document.getElementById("dateContractFilter").value;
  const orgFilters = document.getElementById("orgFilter").value;
  const numberContractFilter = document.getElementById(
    "numberContractFilter"
  ).value;
  if (!dateContractFilter && !orgFilters && !numberContractFilter) {
    return;
  }
  getDataWorks(dateContractFilter, orgFilters, numberContractFilter);
}

function dropWorksFilters() {
  getDataWorks(null, null, null);
}

function getDataWorks(dateContractFilter, orgFilters, numberContractFilter) {
  $.ajax({
    type: "POST",
    url: "/student/works",
    dataSrc: "data",
    data: { dateContractFilter, orgFilters, numberContractFilter },
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

function uploadWork(id) {
  const formData = new FormData();
  const button = document.getElementById("button-upload" + id);
  const file = document.getElementById("input-upload" + id).files[0];
  if (!file) return;
  formData.append("file", file);
  formData.append("work_id", id);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/uploadWorkStudent",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deleteWork(id) {
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idWork: id },
    url: "/deleteWorkStudent",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
  });
}
