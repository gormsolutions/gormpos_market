// Variables to store the modal, header, and close button
const modal = document.getElementById('held-carts-modal');
const modalHeader = document.getElementById('modal-header');
const closeButton = document.getElementById('close-modal');

// Function to open the modal
function openModal() {
    modal.style.display = 'block';
}

// Function to close the modal
function closeModal() {
    modal.style.display = 'none';
}

// Drag functionality for the modal
let isDragging = false;
let offsetX, offsetY;

// When the mouse is pressed down on the header, start the dragging
modalHeader.addEventListener('mousedown', (e) => {
    isDragging = true;
    offsetX = e.clientX - modal.offsetLeft;
    offsetY = e.clientY - modal.offsetTop;

    // Change the cursor to grabbing
    modalHeader.style.cursor = 'grabbing';
});

// When the mouse moves, update the modal's position
document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        const left = e.clientX - offsetX;
        const top = e.clientY - offsetY;
        modal.style.left = `${left}px`;
        modal.style.top = `${top}px`;
    }
});

// When the mouse is released, stop dragging
document.addEventListener('mouseup', () => {
    isDragging = false;
    modalHeader.style.cursor = 'move'; // Reset the cursor
});

// Close the modal when the close button is clicked
closeButton.addEventListener('click', closeModal);

// Function to populate the cart table with dynamic data (mocked for now)
function populateHeldCartsQueue(data) {
    const tableBody = document.getElementById('held-carts').getElementsByTagName('tbody')[0];

    // Clear existing rows
    tableBody.innerHTML = '';

    // Loop through the data to populate the table rows
    data.forEach(cart => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = cart.cart_id;
        row.insertCell(1).textContent = cart.customer;
        row.insertCell(2).textContent = cart.time_held;
        const actionCell = row.insertCell(3);
        const actionButton = document.createElement('button');
        actionButton.textContent = 'Retrieve';
        actionButton.onclick = function() {
            alert('Retrieving cart ' + cart.cart_id);
        };
        actionCell.appendChild(actionButton);
    });
}

// Example data to populate the queue (this could come from an API)
const exampleData = [
    { cart_id: 'CART001', customer: 'John Doe', time_held: '10:30 AM' },
    { cart_id: 'CART002', customer: 'Jane Smith', time_held: '10:45 AM' }
];

// Call the populate function with mock data
populateHeldCartsQueue(exampleData);
