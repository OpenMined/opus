import ApiClient from "./apiClient";

const apiClient = new ApiClient({
  baseUrl: process.env.BASE_URL || "http://localhost:5000",
});
const triggerSideEffect = async ({
  apiCall,
  resultSuccess = (res) => res.status === 200,
  onSuccess = (data) => data,
  onError = () => ({}),
}) => {
  return apiCall()
    .then((response) => {
      if (resultSuccess(response)) {
        return onSuccess(response.data);
      } else {
        return onError(response.data);
      }
    })
    .catch((response) => {
      return onError(response);
    });
};
export { apiClient, triggerSideEffect };
