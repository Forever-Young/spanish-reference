-- Add the build time below the first document title, without changing the source.
local inserted = false
function Header(header)
  if header.level ~= 1 or inserted then
    return nil
  end
  inserted = true
  local timestamp = assert(os.getenv('SPANISH_REFERENCE_BUILT_AT'), 'Missing build timestamp')
  return {
    header,
    pandoc.Div({pandoc.Para({pandoc.Str('Создано: ' .. timestamp)})},
      pandoc.Attr('', {'build-timestamp'}))
  }
end
