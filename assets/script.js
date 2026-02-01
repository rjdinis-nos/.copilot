document.addEventListener('DOMContentLoaded', function() {
  const table = document.querySelector('table');
  const headers = table.querySelectorAll('th');
  const tbody = table.querySelector('tbody');
  
  let sortDirection = {};
  
  headers.forEach((header, index) => {
    if (index === 0 || index === 1) { // Type and Title columns
      header.style.cursor = 'pointer';
      header.style.userSelect = 'none';
      sortDirection[index] = 'asc';
      
      header.addEventListener('click', () => {
        sortTable(index);
        
        // Toggle sort direction
        sortDirection[index] = sortDirection[index] === 'asc' ? 'desc' : 'asc';
        
        // Update visual indicator
        headers.forEach(h => h.textContent = h.textContent.replace(/ [↑↓]/g, ''));
        header.textContent += sortDirection[index] === 'asc' ? ' ↓' : ' ↑';
      });
    }
  });
  
  function sortTable(columnIndex) {
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
      let aValue = a.cells[columnIndex].textContent.trim();
      let bValue = b.cells[columnIndex].textContent.trim();
      
      // For Title column, extract just the title text (before the button)
      if (columnIndex === 1) {
        aValue = aValue.split('\n')[0].trim();
        bValue = bValue.split('\n')[0].trim();
      }
      
      if (sortDirection[columnIndex] === 'asc') {
        return aValue.localeCompare(bValue);
      } else {
        return bValue.localeCompare(aValue);
      }
    });
    
    // Re-append rows in sorted order
    rows.forEach(row => tbody.appendChild(row));
  }
});
