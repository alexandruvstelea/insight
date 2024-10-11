
export const detectPlatform = () => {
  const userAgent = navigator.userAgent;

  const isAndroid = /android/i.test(userAgent);
  const isIOS = /iPad|iPhone|iPod/.test(userAgent);

  return { isAndroid, isIOS };
};
