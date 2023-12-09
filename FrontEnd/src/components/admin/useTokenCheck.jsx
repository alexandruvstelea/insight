
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function useTokenCheck() {
  const router = useRouter();

  const checkToken = () => {
    const token = sessionStorage.getItem('access_token');
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const isExpired = Date.now() >= payload.exp * 1000;

      if (isExpired) {
        toast.error('Tokenul a expirat. Vei fi redirecționat către pagina de login.');
        setTimeout(() => router.push('/adminLogin'), 10000);
        return false;
      }
    } else {
      toast.error('Token-ul nu a fost gasit. Vei fi redirecționat către pagina de login.');
      setTimeout(() => router.push('/adminLogin'), 10000);
      return false;
    }
    return true;
  };

  useEffect(() => {
    if (!checkToken()) {
      return;
    }

    const interval = setInterval(() => {
      if (!checkToken()) {
        clearInterval(interval);
      }
    }, 60000);

    return () => clearInterval(interval);
  }, [router]);
}