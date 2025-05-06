document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.getElementById('submit-button');

    submitButton.addEventListener('click', (e) => {
        // Verhindere, dass das Formular sofort abgeschickt wird (falls du weitere Logik hinzufügst)
        e.preventDefault();

        // Gib eine Erfolgsmeldung aus
        alert("Dein Video wird erstellt! Bitte gedulde dich.");

        // Hier kannst du den Code hinzufügen, um das Formular tatsächlich abzuschicken oder mit einer API zu interagieren.
    });
});
