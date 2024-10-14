
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {

  const roomCode = request.nextUrl.searchParams.get('roomCode');
  // const userAgent = request.headers.get('user-agent') || '';
  // const isAndroid = /android/i.test(userAgent);
  // const isIOS = /iPad|iPhone|iPod/.test(userAgent);

  // if (!isAndroid && !isIOS) {
  //   return NextResponse.redirect(new URL('/wrongDevice', request.url));
  // }

  if (!roomCode) {
    return NextResponse.redirect(new URL('/incorrectURL', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/'], 
};
