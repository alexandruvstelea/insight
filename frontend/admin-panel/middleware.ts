import { NextResponse } from "next/server";
import { NextRequest } from "next/server";
import { fetchCurrentUser } from "./utils/fetchers/currentUser";


export async function middleware(req: NextRequest) {
  
  const token = req.cookies.get("access_token"); 
  const loginPage = new URL("/login", req.url);
  
  if (req.nextUrl.pathname === "/login") {
    if (token) {
      const user = await fetchCurrentUser(); 

      if (user && user.current_user?.role === "admin") {
        return NextResponse.redirect(new URL("/", req.url));
      }else{
        const response = NextResponse.redirect(loginPage);
        response.cookies.set("access_token", "", { expires: new Date(0) });
        return response;
      }
    }
  } 
  if (req.nextUrl.pathname === "/"){
    if (!token) {
      return NextResponse.redirect(loginPage);
    } else {
      const user = await fetchCurrentUser(); 
      
      if (user && user.current_user?.role !== "admin") {
        
        return NextResponse.redirect(loginPage);
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/login"], 
};
