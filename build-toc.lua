-- Build a compact contents page from the main numbered sections.
function Pandoc(doc)
  local entries = {}
  doc:walk({Header = function(header)
    if header.level == 2 then
      entries[#entries + 1] = {
        pandoc.Plain({pandoc.Link(header.content, '#' .. header.identifier)})
      }
    end
  end})
  if #entries == 0 then return doc end
  local toc = pandoc.Div({
    pandoc.Para({pandoc.Strong({pandoc.Str('Содержание')})}),
    pandoc.BulletList(entries)
  }, pandoc.Attr('table-of-contents', {'table-of-contents'}))
  for i, block in ipairs(doc.blocks) do
    if block.t == 'Div' and block.classes:includes('build-timestamp') then
      doc.blocks:insert(i + 1, toc)
      return doc
    end
  end
  doc.blocks:insert(1, toc)
  return doc
end
