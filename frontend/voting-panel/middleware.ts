
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {

  const roomCode = request.nextUrl.searchParams.get('roomCode');
  // const userAgent = request.headers.get('user-agent') || '';
  // const isAndroid = /android/i.test(userAgent);
  // const isIOS = /iPad|iPhone|iPod/.test(userAgent);

  // if (!isAndroid && !isIOS) {
  //   return NextResponse.redirect('https://www.google.com');
  // }

  if (!roomCode) {
    return NextResponse.redirect('https://www.google.com');
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/'], 
};
