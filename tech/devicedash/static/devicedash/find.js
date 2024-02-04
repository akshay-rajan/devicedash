// document.addEventListener('DOMContentLoaded', () => {

//   // Viewphones
//   let viewphones = document.getElementsByClassName('viewphone');
//   for (let i = 0; i < viewphones.length; i++) {
//     let viewbutton = viewphones[i];
//     viewbutton.addEventListener('click', () => displayPhone(viewbutton));
//   }

//   // Backbutton
//   let backButton = document.querySelector('.backbutton');

//   let phoneListDiv = document.getElementById('phonelist');
//   let viewPhoneDiv = document.getElementById('viewphone');

//   // Back to the results
//   if (backButton) {
//     backButton.addEventListener('click', () => {
//       phoneListDiv.style.display = 'block';
//       viewPhoneDiv.style.display = 'none';
//     });
//   }
// })


// function displayPhone(viewbutton) {

//   // Display the phone in detail
//   let phone_id = viewbutton.dataset.id;
//   console.log(phone_id);
//   fetch('view.html')
//     .then(response => response.text())
//     .then(html => {
//         phoneListDiv.innerHTML = html;
//     })
//     .catch(error => console.error('Error loading page:', error));

//   // Hide and Show the appropriate divs
//   let phoneListDiv = document.getElementById('phonelist');
// //   let viewPhoneDiv = document.getElementById('viewphone');
//   phoneListDiv.style.display = 'none';
//   viewPhoneDiv.style.display = 'block';
  
//   // Display the Details
//   viewPhoneDiv.innerHTML = '<button>heyyy</button>';
//     // Create 'Back' button
//   let backButton = document.querySelector('.backbutton');
//   if (!backButton) {
//     backButton = document.createElement('button');
//     backButton.classList.add('btn', 'btn-primary', 'backbutton');
//     backButton.textContent = "Back";
//     viewPhoneDiv.appendChild(backButton);
//   }
//   backButton.addEventListener('click', () => {
//     phoneListDiv.style.display = 'block';
//     viewPhoneDiv.style.display = 'none';
//   });
// }

