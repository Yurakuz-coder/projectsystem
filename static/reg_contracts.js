function applyContractsFilters(page) {
  const dateContractFilter =
    document.getElementById("dateContractFilter")?.value;
  const orgFilters = document.getElementById("orgFilter")?.value;
  const numberContractFilter = document.getElementById(
    "numberContractFilter"
  )?.value;
  if (page == undefined && !dateContractFilter && !orgFilters && !numberContractFilter) {
    return;
  }
  getDataContract(page, dateContractFilter, orgFilters, numberContractFilter);
}

function dropContractFilters() {
  const dateContractFilter =
    document.getElementById("dateContractFilter");
  const orgFilters = document.getElementById("orgFilter");
  const numberContractFilter = document.getElementById(
    "numberContractFilter"
  );
  dateContractFilter && (dateContractFilter.value = "")
  orgFilters && (orgFilters.value = "")
  numberContractFilter && (numberContractFilter.value = "")
  getDataContract(null, null, null, null);
}

function getDataContract(page, dateContractFilter, orgFilters, numberContractFilter) {
  $.ajax({
    type: "POST",
    url: "/admin/contracts",
    dataSrc: "data",
    data: { page, dateContractFilter, orgFilters, numberContractFilter },
    success: function (data) {
      const resultTable = document.getElementById("resultTable");
      resultTable.innerHTML = data;
      const table = document.getElementById("collapseTableBody");
      table.className = "collapse show";
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function getDocument(id) {
  $.ajax({
    type: "GET",
    data: { contractId: id },
    url: "/getContractSigned",
  });
}

function uploadFile(id) {
  const formData = new FormData();
  const button = document.getElementById("button-upload" + id);
  const buttonName = button.id;
  const file = document.getElementById("input-upload" + id).files[0];
  if (!file) return;
  formData.append("file", file);
  formData.append("contract_id", id);
  const url = window.location.pathname.split("/")[1];
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/" + url + "/uploadContractSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
      document.getElementById(buttonName).innerHTML = 'Файл загружен!';
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deleteFile(id) {
  const button = document.getElementById("button-delete" + id);
  const buttonName = button.id;
  const url = window.location.pathname.split("/")[1];
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idContract: id },
    url: "/" + url + "/deleteContractSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
      document.getElementById(buttonName).innerHTML = 'Файл удален!';
    },
    error: function () {
      document.getElementById(buttonName).innerHTML.innerHTML = "Файл не удален!";
    },
  });
}
