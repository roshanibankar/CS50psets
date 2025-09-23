document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  load_mailbox('inbox');
});

function compose_email() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view')?.remove(); 

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#email-detail-view')?.remove();

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {
        const div = document.createElement('div');
        div.className = 'email-item';
        div.style.backgroundColor = email.read ? '#f0f0f0' : 'white';
        div.style.cursor = 'pointer';

        div.innerHTML = `
          <strong>${mailbox === 'sent' ? 'To' : 'From'}:</strong> ${mailbox === 'sent' ? email.recipients.join(', ') : email.sender}
          <strong>Subject:</strong> ${email.subject}
          <span style="float: right;">${email.timestamp}</span>
        `;

        div.addEventListener('click', () => view_email(email.id, mailbox));
        document.querySelector('#emails-view').append(div);
      });
    });
}

function send_email(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({ recipients, subject, body })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    });
}


function view_email(id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ read: true })
      });

      let detail = document.createElement('div');
      detail.id = 'email-detail-view';
      detail.innerHTML = `
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
        <p><strong>Subject:</strong> ${email.subject}</p>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        <hr>
        <p>${email.body.replace(/\n/g, "<br>")}</p>
      `;

      // Reply button
      const reply = document.createElement('button');
      reply.innerText = 'Reply';
      reply.className = 'btn btn-sm btn-outline-primary mr-2';
      reply.addEventListener('click', () => {
        compose_email();
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
        document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
      });
      detail.append(reply);

      // Archive / Unarchive
      if (mailbox !== 'sent') {
        const archive = document.createElement('button');
        archive.innerText = email.archived ? 'Unarchive' : 'Archive';
        archive.className = 'btn btn-sm btn-outline-secondary ml-2';
        archive.addEventListener('click', () => {
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ archived: !email.archived })
          }).then(() => load_mailbox('inbox'));
        });
        detail.append(archive);
      }

      document.querySelector('body').append(detail);
    });
}

