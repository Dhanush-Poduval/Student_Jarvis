import Navbar from "@/components/dashboard/Navbar"
import AppSidebar from "@/components/dashboard/Sidebar"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"


export default function Layout({children}) {
  return (
    <SidebarProvider>
      <AppSidebar />
      
        <div className="w-full">
            <Navbar />
           <div className="mt-10 px-4">
            {children}
            </div> 
        </div>
        
      
    </SidebarProvider>
  )
}