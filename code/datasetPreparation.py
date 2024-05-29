from xml.dom import minidom


def create_xml(path, img, width, height, boxes) -> None:
    boundaries = ['xmin', 'ymin', 'xmax', 'ymax']

    doc = minidom.Document()
    parent = doc.createElement('annotation')
    doc.appendChild(parent)

    child = doc.createElement('folder')
    child.appendChild(doc.createTextNode('FOLDER_TBD'))
    parent.appendChild(child)

    child = doc.createElement('filename')
    child.appendChild(doc.createTextNode(f'{img}'))
    parent.appendChild(child)

    child = doc.createElement('path')
    child.appendChild(doc.createTextNode('PATH_TBD'))
    parent.appendChild(child)

    child = doc.createElement('source')
    child2 = child.appendChild(doc.createElement('database'))
    child2.appendChild(doc.createTextNode('Unknown'))
    parent.appendChild(child)

    child = doc.createElement('size')
    child2 = child.appendChild(doc.createElement('width'))
    child2.appendChild(doc.createTextNode(f'{width}'))
    child3 = child.appendChild(doc.createElement('height'))
    child3.appendChild(doc.createTextNode(f'{height}'))
    child4 = child.appendChild(doc.createElement('depth'))
    child4.appendChild(doc.createTextNode('1'))
    parent.appendChild(child)

    child = doc.createElement('segmented')
    child.appendChild(doc.createTextNode('0'))
    parent.appendChild(child)

    for box in boxes:
        child = doc.createElement('object')
        grandchild1 = child.appendChild(doc.createElement('name'))
        grandchild1.appendChild(doc.createTextNode(box[0]))
        grandchild2 = child.appendChild(doc.createElement('pose'))
        grandchild2.appendChild(doc.createTextNode('Unspecified'))
        grandchild3 = child.appendChild(doc.createElement('truncated'))
        grandchild3.appendChild(doc.createTextNode('0'))
        grandchild4 = child.appendChild(doc.createElement('difficult'))
        grandchild4.appendChild(doc.createTextNode('0'))

        grandchild5 = child.appendChild(doc.createElement('bndbox'))
        for i, boundary in enumerate(boundaries):
            grandgrandchild = grandchild5.appendChild(doc.createElement(boundary))
            grandgrandchild.appendChild(doc.createTextNode(str(box[i+1])))
        parent.appendChild(child)

    xml_str = doc.toprettyxml(indent="\t")
    save_path_file = f"{path}{img}.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)

    return None
