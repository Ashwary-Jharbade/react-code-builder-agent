import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';

// Define the mutation function to add or update an item
const addItem = async (queryClient, newItem) => {
  // Simulate a server-side API call. In a real application, this would be an actual HTTP request.
  const response = await fetch('/api/items', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(newItem)
  });
  return response.json();
};

const updateItem = async (queryClient, updatedItem) => {
  // Simulate a server-side API call. In a real application, this would be an actual HTTP request.
  const response = await fetch(`/api/items/${updatedItem.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updatedItem)
  });
  return response.json();
};

function App() {
  const [name, setName] = useState('');
  const queryClient = useQueryClient();

  // Use the mutation hook to create a new item
  const { mutate: addItemMutation } = useMutation('addItem', (newItem) => addItem(queryClient, newItem));

  // Use the mutation hook to update an existing item
  const { mutate: updateItemMutation, isLoading: isUpdating } = useMutation('updateItem', (updatedItem) => updateItem(queryClient, updatedItem));

  return (
    <div>
      <h1>React Query Mutation Example</h1>
      <form onSubmit={(e) => {
        e.preventDefault();
        if (!name.trim()) return;
        
        // Create a new item
        const newItem = { id: Date.now(), name };
        addItemMutation(newItem);
        
        // Clear the input after adding the item
        setName('');
      }}>
        <input
          type='text'
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder='Enter a new item'
          required
        />
        <button type='submit' disabled={isUpdating}>
          {isUpdating ? 'Adding...' : 'Add Item'}
        </button>
      </form>
      
      {/* Display some sample items */}
      <div>
        <h2>Items</h2>
        <ul>
          <li data-testid='item-1'>Item 1</li>
          <li data-testid='item-2'>Item 2</li>
        </ul>
      </div>

      {/* Example of updating an existing item */}
      {isUpdating && (
        <p>Updating...</p>
      )}
    </div>
  );
}

export default App;
