import {useRef, useState} from 'react';
import {flushSync} from 'react-dom';
import {createRoot} from 'react-dom/client';

const labels = {
  provided: 'Có thông tin',
  missing: 'Còn thiếu',
  unclear: 'Chưa rõ',
  conflicting: 'Mâu thuẫn'
};
const emptyField = {value: null, status: 'missing', source_refs: [], user_confirmed: false};
const statusIcons = {provided: '●', missing: '○', unclear: '◐', conflicting: '◐'};

function statusOf(field, resolved) {
  if (!field) return 'missing';
  return field.status === 'provided' && !resolved(field) ? 'unclear' : field.status;
}

function Citations({field, caption, sourceTypes}) {
  if (!field.source_refs.length) return null;
  return (
    <details className="citations">
      <summary>{caption} ({field.source_refs.length})</summary>
      <ul>
        {field.source_refs.map((source, index) => (
          <li key={index}>
            {[
              `[${source.source_id}] ${sourceTypes[source.source_type] || source.source_type}`,
              source.locator,
              source.quote && `“${source.quote}”`
            ].filter(Boolean).join(' · ')}
          </li>
        ))}
      </ul>
    </details>
  );
}

function DraftField({entry, filter, history, resolved, sourceTypes, precisionTypes, onSave, onConfirm, filterRef}) {
  const field = entry.field || emptyField;
  const present = resolved(field);
  const value = field.value || '';
  const status = statusOf(field, resolved);
  const [editing, setEditing] = useState(false);
  const [pending, setPending] = useState('');
  const input = useRef(null);
  const edit = useRef(null);
  const changed = pending.trim() !== value.trim();
  const canKeep = !present && Boolean(value.trim());
  const hidden = filter !== 'all' && filter !== status;
  const previous = history.get(entry.path) || [];

  function toggleEdit() {
    if (editing) {
      setEditing(false);
      return;
    }
    setPending(value);
    flushSync(() => setEditing(true));
    input.current.focus();
  }

  function save() {
    flushSync(() => setEditing(false));
    onSave(entry, pending.trim());
    (edit.current.closest('.field').hidden ? filterRef.current : edit.current).focus();
  }

  return (
    <div className="field" data-status={status} hidden={hidden}>
      <div className="field-top">
        <label htmlFor={`field-${entry.path}`}>{entry.label}</label>
        <span className="badge" data-status={status} id={`status-${entry.path}`}>
          <span aria-hidden="true">{statusIcons[status]}</span> {labels[status]}
        </span>
      </div>
      {value && <p className="field-value" hidden={editing}>{value}</p>}
      <textarea
        id={`field-${entry.path}`} ref={input} hidden={!editing} value={pending}
        aria-describedby={`status-${entry.path}`} onChange={event => setPending(event.target.value)}
        rows={Math.max(2, Math.min(4, value.split('\n').length))}
      />
      {field.conflict_note && <p className="conflict">{field.conflict_note}</p>}
      {field.precision && <p className="help metadata">Độ chính xác: {precisionTypes[field.precision]}</p>}
      <Citations field={field} caption="Xem nguồn" sourceTypes={sourceTypes} />
      {previous.length > 0 && (
        <details className="citations">
          <summary>Xem thông tin trước khi sửa</summary>
          {previous.map((item, index) => (
            <div key={index}>
              <p>{labels[item.status]} · {item.value || 'Chưa có giá trị'}</p>
              {item.conflict_note && <p className="conflict">{item.conflict_note}</p>}
              <Citations field={item} caption="Nguồn trước khi sửa" sourceTypes={sourceTypes} />
            </div>
          ))}
        </details>
      )}
      <div className="actions">
        <button type="button" className="edit-field" ref={edit} onClick={toggleEdit}
          aria-expanded={editing} aria-controls={`field-${entry.path}`}>
          {editing ? 'Hủy chỉnh sửa' : value ? 'Chỉnh sửa' : 'Bổ sung'}
        </button>
        {editing && (
          <button type="button" className="secondary" onClick={save} disabled={!changed && !canKeep}>
            {!changed && canKeep ? 'Dùng giá trị này' : 'Lưu chỉnh sửa'}
          </button>
        )}
        {present && (
          <label className="choice">
            <input type="checkbox" checked={field.user_confirmed} disabled={editing}
              aria-label={`Xác nhận ${entry.title}`} onChange={event => onConfirm(entry, event.target.checked)} />
            Tôi xác nhận thông tin này
          </label>
        )}
      </div>
    </div>
  );
}

function DraftFields({groups, resolved, ...fieldProps}) {
  const [filter, setFilter] = useState('all');
  const filterRef = useRef(null);
  const listRef = useRef(null);
  const matches = groups.map(group => group.fields.filter(({field}) => filter === 'all' || statusOf(field, resolved) === filter).length);
  const count = matches.reduce((total, size) => total + size, 0);

  function changeFilter(event) {
    const value = event.target.value;
    setFilter(value);
    if (value !== 'all') {
      for (const group of listRef.current.children) {
        if (group.querySelector(`.field[data-status="${value}"]`)) group.open = true;
      }
    }
  }

  return (
    <>
      <div className="filterbar">
        <label htmlFor="field-filter">Hiển thị</label>
        <select id="field-filter" value={filter} ref={filterRef} onChange={changeFilter}>
          <option value="all">Tất cả các trường</option>
          <option value="conflicting">Có mâu thuẫn</option>
          <option value="missing">Còn thiếu</option>
          <option value="unclear">Chưa rõ</option>
          <option value="provided">Có thông tin</option>
        </select>
        <span id="filter-count" role="status" className="help">{count ? `${count} trường` : 'Không có trường phù hợp.'}</span>
      </div>
      <div ref={listRef}>
        {groups.map((group, index) => {
          const missingCount = group.fields.filter(({field}) => statusOf(field, resolved) !== 'provided').length;
          return (
            <details className="document" key={group.id} open={group.initiallyOpen} hidden={!matches[index]}>
              <summary>
                <span>{group.title}</span>
                {missingCount > 0 && <span className="badge" data-status="missing">{missingCount} còn thiếu</span>}
              </summary>
              <div className="field-list">
                {group.metadata?.map(text => <p className="help metadata" key={text}>{text}</p>)}
                {group.fields.map(entry => (
                  <DraftField key={entry.path} {...fieldProps} {...{entry, filter, resolved, filterRef}} />
                ))}
                {group.footer && <p className="help metadata">{group.footer}</p>}
              </div>
            </details>
          );
        })}
      </div>
    </>
  );
}

export function mount(container) {
  const root = createRoot(container);
  return (revision, props) => flushSync(() => root.render(<DraftFields key={revision} {...props} />));
}
