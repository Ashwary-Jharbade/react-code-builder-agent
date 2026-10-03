const useMutation = (mutationFn) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mutation = async (variables) => {
    try {
      setLoading(true);
      const result = await mutationFn(variables);
      setData(result.data);
      return { data: result.data };
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  return {
    mutate: mutation,
    data,
    loading,
    error,
  };
}