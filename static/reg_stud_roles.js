function getRoles(id) {
  $.ajax({
    type: "GET",
    url: "/student/getRoles",
    data: { id },
    success: function (data) {
      const select = document.getElementById("role");
      const button = document.getElementById("studentTicketButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Роли не найдены", 0));
        select.disabled = true;
        button.disabled = true;
        return;
      }
      select.disabled = false;
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(`${item.rolesRole} #${item.rolesFunction}`, item.IDroles)
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}
