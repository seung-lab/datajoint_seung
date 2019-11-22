function obj = getSchema
persistent schemaObject
if isempty(schemaObject)
    schemaObject = dj.Schema(dj.conn, 'pinky', 'Seung_pinky');
end
obj = schemaObject;
end
