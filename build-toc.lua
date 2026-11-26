-- Build a compact contents page: parts (bold, indented sections below) and numbered sections.
function Pandoc(doc)
  local groups = {}   -- { {title = inlines, items = {...}} }, parts in order
  local loose = {}
  local current = nil
  doc:walk({Header = function(header)
    if header.level == 1 and header.classes:includes('part') then
      current = {title = header.content, items = {}}
      groups[#groups + 1] = current
    elseif header.level == 2 then
      local item = {pandoc.Plain({pandoc.Link(header.content, '#' .. header.identifier)})}
      if current then
        current.items[#current.items + 1] = item
      else
        loose[#loose + 1] = item
      end
    end
  end})
  local entries = loose
  for _, g in ipairs(groups) do
    entries[#entries + 1] = {
      pandoc.Plain({pandoc.Strong(g.title)}),
      pandoc.BulletList(g.items)
    }
  end
  if #entries == 0 then return doc end
  local toc = pandoc.Div({
    pandoc.Para({pandoc.Strong({pandoc.Str('Содержание')})}),
    pandoc.BulletList(entries)
  }, pandoc.Attr('table-of-contents', {'table-of-contents'}))
  for _, cls in ipairs({'ai-note', 'build-timestamp'}) do
    for i, block in ipairs(doc.blocks) do
      if block.t == 'Div' and block.classes:includes(cls) then
        doc.blocks:insert(i + 1, toc)
        return doc
      end
    end
  end
  doc.blocks:insert(1, toc)
  return doc
end
