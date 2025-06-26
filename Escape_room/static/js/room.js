document.addEventListener('DOMContentLoaded', function() {
  function attachListeners() {
    // Creepy shake on click
    document.querySelectorAll('.answer-box').forEach(function(box) {
      box.addEventListener('click', function() {
        this.classList.remove('clicked');
        void this.offsetWidth;
        this.classList.add('clicked');
      });
    });

    // AJAX form submit
    const form = document.getElementById('answer-form');
    if (form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        const qaContainer = document.querySelector('.qa-container');
        const formData = new FormData(form);

        fetch(window.location.href, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          if (data.correct) {
            // Fade out
            qaContainer.classList.add('fade-out');
            setTimeout(() => {
              if (data.finished) {
                qaContainer.innerHTML = "<h2>You survived!</h2>";
              } else {
                qaContainer.innerHTML = `
                  <h2>${data.next_name}</h2>
                  <p><strong>Riddle:</strong> ${data.next_question}</p>
                  <p>${data.next_description}</p>
                  <form id="answer-form" method="post">
                    <input type="text" name="answer" placeholder="Make your guess" class="answer-box">
                    <button type="submit">Submit</button>
                  </form>
                `;
              }
              qaContainer.classList.remove('fade-out');
              qaContainer.classList.add('fade-in');
              setTimeout(() => qaContainer.classList.remove('fade-in'), 700);
              attachListeners(); // Re-attach listeners to new elements
            }, 700);
          } else {
            // Jumpscare on wrong answer
            const jumpscare = document.getElementById('jumpscare');
            const audio = document.getElementById('jumpscare-audio');
            if (jumpscare && audio) {
              jumpscare.style.display = 'flex';
              audio.play();
              setTimeout(() => {
                jumpscare.style.display = 'none';
                audio.pause();
                audio.currentTime = 0;
              }, 1500); // 1.5 seconds
            }
          }
        });
      });
    }
  }

  attachListeners();
});