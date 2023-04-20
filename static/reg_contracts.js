function applyContractsFilters() {
  const dateContractFilter =
    document.getElementById("dateContractFilter").value;
  const orgFilters = document.getElementById("orgFilter").value;
  const numberContractFilter = document.getElementById(
    "numberContractFilter"
  ).value;
  if (!dateContractFilter && !orgFilters && !numberContractFilter) {
    return;
  }
  getDataContract(dateContractFilter, orgFilters, numberContractFilter);
}

function dropContractFilters() {
  getDataContract(null, null, null);
}

function getDataContract(dateContractFilter, orgFilters, numberContractFilter) {
  $.ajax({
    type: "POST",
    url: "/admin/contracts",
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
  const file = document.getElementById("input-upload" + id).files[0];
  if (!file) return;
  formData.append("file", file);
  formData.append("contract_id", id);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/uploadContractSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deleteFile(id) {
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idContract: id },
    url: "/deleteContractSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
  });
}
