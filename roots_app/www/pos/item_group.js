// // Function to fetch and populate item groups dynamically
// async function fetchItemGroups() {
//     try {
//         // Fetch all item groups (this should be done through an API call if you don't have the groups)
//         const response = await fetch('/api/method/roots_app.custom_api.supermarket.items.get_item_groups');
        
//         if (response.ok) {
//             const result = await response.json();
//             const itemGroups = result.message.item_groups || []; // Ensure item_groups is an array
//             populateItemGroups(itemGroups); // Populate dropdown with item groups
//         } else {
//             console.error("Error fetching item groups:", response.statusText);
//         }
//     } catch (error) {
//         console.error("Error fetching item groups:", error);
//     }
// }

// // Function to populate item groups in the dropdown
// function populateItemGroups(itemGroups) {
//     const itemGroupDropdown = document.getElementById('item-group');
    
//     // Clear existing options
//     itemGroupDropdown.innerHTML = '<option value="">Select Item Group</option>';

//     // Populate dropdown with item groups
//     itemGroups.forEach(group => {
//         const option = document.createElement('option');
//         option.value = group.name;
//         option.textContent = group.name;
//         itemGroupDropdown.appendChild(option);
//     });

//     // Add an event listener to filter items based on selected group
//     itemGroupDropdown.addEventListener('change', function() {
//         filterItemsByGroup(this.value); // When the item group changes, filter the items
//     });
// }

// // Function to fetch and display items based on the selected item group
// async function filterItemsByGroup(itemGroup) {
//     const searchTerm = document.getElementById('item-search').value;

//     try {
//         // Fetch data from the Frappe API, passing the selected item group and search term
//         const response = await fetch(`/api/method/roots_app.custom_api.supermarket.items.get_items?search_term=${searchTerm}&category=${itemGroup}`);

//         if (response.ok) {
//             const result = await response.json();
//             const items = result.message.items || []; // Ensure items is an array

//             // Display filtered items
//             displayItems(items);
//         } else {
//             console.error("Error fetching items:", response.statusText);
//         }
//     } catch (error) {
//         console.error("Error fetching items:", error);
//     }
// }

// // Function to display items as cards
// function displayItems(items) {
//     const itemsContainer = document.getElementById('items-container');
//     itemsContainer.innerHTML = ''; // Clear existing items

//     if (items.length > 0) {
//         items.forEach(item => {
//             const card = document.createElement('div');
//             card.classList.add('item-card');

//             // Item Card Content
//             card.innerHTML = `
//                 <img src="${item.image || 'default.jpg'}" alt="${item.name}" />
//                 <div class="item-name">${item.name}</div>
//                 <div class="item-price">$${item.price}</div>
//                 <button onclick="addToCart('${item.id}', '${item.name}', ${item.price})">Add to Cart</button>
//             `;

//             itemsContainer.appendChild(card);
//         });
//     } else {
//         itemsContainer.innerHTML = '<p>No items available in this group.</p>';
//     }
// }

// // Trigger fetchItemGroups on page load to populate the item group dropdown
// window.onload = function () {
//     fetchItemGroups(); // Fetch and populate item groups
// };
