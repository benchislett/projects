module FractalRender

  using CSFML.LibCSFML

  include("./state.jl")
  include("./colors.jl")
  include("./simulate.jl")
  include("./render.jl")

  function main()
    width = 1000
    height = 1000
    zoom = 0.5
    iterations=100
    renderState = RenderState(width=width, height=height)
    simState = State(res=(width,height), iterations=iterations)

    i = 0

    step!(simState)
    update!(simState, renderState)

    event = Ref{sfEvent}()
    while Bool(sfRenderWindow_isOpen(renderState.window))

      while Bool(sfRenderWindow_pollEvent(renderState.window, event))
        if event.x.type == sfEvtClosed
          sfImage_saveToFile(sfRenderWindow_capture(renderState.window), "output/output.png")
          sfRenderWindow_close(renderState.window)
        end
      end

      if Bool(sfMouse_isButtonPressed(sfMouseLeft))
        pos = sfMouse_getPositionRenderWindow(renderState.window)
        
        println("Mouse event registered at: ", pos)

        if pos.x in 1:width && pos.y in 1:height
          println("Valid mouse event. Zooming...")
          dx = pos.x / width
          dy = pos.y / height

          newbounds = (
          (
            simState.bounds[1][1] + zoom * dx * simState.lengths[1],
            simState.bounds[1][2] - zoom * (1 - dx) * simState.lengths[1]
          ),
          (
            simState.bounds[2][1] + zoom * dy * simState.lengths[2],
            simState.bounds[2][2] - zoom * (1 - dy) * simState.lengths[2]
          ))

          simState.bounds = newbounds
          updateState!(simState)
          step!(simState)
          update!(simState, renderState)
        end
      end

      render!(simState, renderState)

      i += 1
    end
  end
end

FractalRender.main()

