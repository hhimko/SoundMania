import pygame

from view.baseview import View


class MapPlayerView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        

    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                pass
                
            
    def update(self, dt: int) -> None:
        pass
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        surface.fill((255, 0, 0))
        
        
    def on_window_resize(self) -> None:
        pass