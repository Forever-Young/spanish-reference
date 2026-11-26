-- Add the build time below the first document title, without changing the source.
local inserted = false
function Header(header)
  if header.level ~= 1 or inserted then
    return nil
  end
  inserted = true
  -- Split "Title: subtitle" into a title and a smaller subtitle line.
  local text = pandoc.utils.stringify(header)
  local main, sub = text:match('^(.-):%s*(.+)$')
  if main then
    sub = pandoc.text.upper(pandoc.text.sub(sub, 1, 1)) .. pandoc.text.sub(sub, 2)
    header.content = {
      pandoc.Str(main),
      pandoc.Span({pandoc.Str(sub)}, pandoc.Attr('', {'subtitle'}))
    }
  end
  local timestamp = assert(os.getenv('SPANISH_REFERENCE_BUILT_AT'), 'Missing build timestamp')
  return {
    header,
    pandoc.Div({pandoc.Para({pandoc.Str('Создано: ' .. timestamp)})},
      pandoc.Attr('', {'build-timestamp'}))
  }
end
