function sendMail() {
  const admin = document.getElementById('admin').value
  const subject = document.getElementById('subject').value
  const message = document.getElementById('message').value
  const files = document.getElementById('attachedFiles').files[0]
  const button = document.getElementById('sendMailButton')
  const formData = new FormData();
  formData.append("files", files);
  formData.append("message", message);
  formData.append("subject", subject);
  formData.append("admin", admin);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/sendmailtoadmin",
    success: function () {
      button.innerHTML = 'Сообщение отправлено';
    },
    error: function () {
      button.innerHTML = "Произошла ошибка при отправке!";
    },
  });
}

function changeIniciator(idInic) {
  $.ajax({
    type: "GET",
    url: "/getIniciatorMail",
    data: { idInic },
    success: function (data) {
      const select = document.getElementById('admin');
      const button = document.getElementById("sendMailButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Инициаторы не найдены", 0));
        button.disabled = true
        return;
      }
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(
            `${item[2]} (${item[1]}) - ${item[3]}`,
            item[0]
          )
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function changeSheffOrg(idOrg) {
  $.ajax({
    type: "GET",
    url: "/getSheffOrgMail",
    data: { idOrg },
    success: function (data) {
      const select = document.getElementById('admin');
      const button = document.getElementById("sendMailButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Руководители не найдены", 0));
        button.disabled = true
        return;
      }
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(
            `${item[2]} (${item[1]}) - ${item[3]}`,
            item[0]
          )
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function changeStudent(idProject) {
  $.ajax({
    type: "GET",
    url: "/getStudentsMail",
    data: { idProject },
    success: function (data) {
      const select = document.getElementById('admin');
      const button = document.getElementById("sendMailButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Студенты не найдены", 0));
        select.disabled = true;
        button.disabled = true;
        return;
      }
      select.disabled = false;
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(
            `${item[0]} (${item[2]})`,
            item[1]
          )
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function changeSheffProj(idProject) {
  $.ajax({
    type: "GET",
    url: "/getSheffProjMail",
    data: { idProject },
    success: function (data) {
      const select = document.getElementById('admin');
      const button = document.getElementById("sendMailButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Руководители не найдены", 0));
        button.disabled = true
        return;
      }
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(
            `${item[0]}`,
            item[1]
          )
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}
