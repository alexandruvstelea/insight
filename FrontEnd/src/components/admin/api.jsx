

export const deleteItem = async (url, id, fetchFunction) => {
  const token = sessionStorage.getItem('access_token');
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/${url}/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`Failed to delete ${url.slice(0, -1)}`);
    }
    fetchFunction();
  } catch (err) {
    console.error(`Error deleting ${url.slice(0, -1)}:`, err);
  }
};

