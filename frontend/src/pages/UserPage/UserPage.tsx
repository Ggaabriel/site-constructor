import React, { useContext, useEffect, useState } from "react";
import { useAppDispatch } from "src/app/hooks/useAppDispatch";
import { useAppSelector } from "src/app/hooks/useAppSelector";
import useGetTree from "src/app/hooks/useGetTree";
import {
  deleteNode,
  setCoreNewChild,
  setExistNewChild,
  setTree,
  setChildrens,
  updateNode,
} from "src/app/store/slice/UserPgaeSlice";
import {
  useDeleteNodesMutation,
  useLazyGetNodesQuery,
  usePatchAttrMutation,
  usePatchNodesMutation,
  usePostNodesMutation,
  usePostPageMutation,
} from "src/app/store/slice/UserPgaeSlice/UserPageApi";
import { AddButton } from "src/shared/AddButton/AddButton";
import Back from "src/app/assets/icons/back.svg?react";
import Trash from "src/app/assets/icons/trash.svg?react";
import Return from "src/app/assets/icons/return.svg?react";
import Exit from "src/app/assets/icons/exit.svg?react";
import Edit from "src/app/assets/icons/edit.svg?react";
import { useNavigate, useParams } from "react-router-dom";
import { menuContext } from "src/app/context";
import { AnimatePresence, Reorder, motion } from "framer-motion";
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "src/shared/ui/ui/drawer";
import { ITreeNode } from "src/app/types/nodes";
import { axiosBase } from "src/app/http";
import { useQueryClient } from "react-query";
import { InputDefault } from "src/shared/InputDefault/InputDefault";
import { LinkButton } from "src/shared/LinkButton/LinkButton";
import Alignment from "src/widgets/Alignment/Alignment";
import BgAlignment from "src/widgets/Alignment/BgAlignment";
import Upload from "src/app/assets/icons/upload.svg?react";
import Container from "src/app/assets/icons/container.svg?react";
import Text from "src/app/assets/icons/textEdit.svg?react";
import Image from "src/app/assets/icons/imageEdit.svg?react";
import Save from "src/app/assets/icons/save.svg?react";

const UserPage: React.FC = () => {
  const [align, setAlign] = useState<string>("text-left");
  const [bgAlign, setBgAlign] = useState<string>("flex-col");
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { projectId } = useParams();
  const nodes = useAppSelector((state) => state.userPage);
  const { tree, isTreeSuccess, getIdByType } = useGetTree<ITreeNode>(
    projectId!,
  );
  const [patchNodes] = usePatchNodesMutation();
  const { setMenuItems } = useContext(menuContext);
  const [deleteNodes] = useDeleteNodesMutation();
  const queryClient = useQueryClient();
  const [selectedType, setSelectedType] = useState<
    "container" | "text" | "image" | null
  >(null);
  const [animate, setAnimate] = useState(false);
  const [nodeText, setNodeText] = useState<string>("");

  interface IAttribute {
    node_id: string;
    attribute_name: string;
    attribute_value: string;
    holder?: boolean;
  }
  const [postPage] = usePostPageMutation();
  const setBaseMenu = () => {
    const menuItem = [
      {
        handleClick: () => navigate(-1),
        Image: Exit,
      },
      {
        handleClick: () => postPage({ projectId }),
        Image: Save,
      },
    ];
    setMenuItems(menuItem);
  };

  useEffect(() => {
    setBaseMenu();
    if (isTreeSuccess && tree) {
      dispatch(setTree(tree));
    }
  }, [isTreeSuccess, dispatch, tree, navigate, setMenuItems]);

  const [postNodes] = usePostNodesMutation();
  const [getNodes] = useLazyGetNodesQuery();
  const [patchAttr] = usePatchAttrMutation();
  const addNode = async (id: string, type: string) => {
    const { data: newId } = (await postNodes({
      parent: id,
      template_id: type,
    })) as { data: string };
    const { data } = await getNodes(newId);

    const newChild: Partial<ITreeNode> = {
      id: newId,
      attrs: data.attrs,
      type_id: data.type_id,
      children: [],
    };
    dispatch(setExistNewChild({ newChild: newChild, id: id }));
    return newId;
  };

  const addCoreNode = async (id: string, type: string) => {
    const { data: newId } = (await postNodes({
      parent: id,
      template_id: type,
    })) as { data: string };
    const { data } = await getNodes(newId);

    const newChild: Partial<ITreeNode> = {
      id: newId,
      attrs: data.attrs,
      type_id: data.type_id,
      children: [],
    };
    dispatch(setCoreNewChild(newChild));
    return newId;
  };
  const patchNode = async (attribute: IAttribute) => {
    await patchAttr(attribute);
    const { data } = await getNodes(attribute.node_id);
    const newChild = {
      attrs: await data.attrs,
      type_id: await data.type_id,
      children: nodeInfo !== null ? nodeInfo.children : [],
      holder: attribute.holder,
    };
    dispatch(updateNode({ id: attribute.node_id, updatedValues: newChild }));
  };
  const handleDeleteNode = (id: string) => {
    deleteNodes(id);
    dispatch(deleteNode(id));
  };
  const [activeItemChoice, setActiveItemChoice] = useState("");
  type Tevent = {
    target: {
      elements: {
        color: {
          value: string;
        };
      };
    };
  };
  type NodeInfo = {
    newId: string;
    type: string;
  };
  const handleSubmit = async (
    event: SubmitEvent | Tevent | React.FormEvent<HTMLFormElement>,
    { newId, type }: NodeInfo,
  ) => {
    const targetEvent: Tevent = event as Tevent;

    const color = targetEvent.target.elements.color.value;
    if (type == "text") {
      const text = {
        node_id: newId,
        attribute_name: "text",
        attribute_value: nodeText,
        holder: false,
      };
      await patchNode(text);
      const position = {
        node_id: newId,
        attribute_name: "position",
        attribute_value: align,
        holder: false,
      };
      await patchNode(position);
      const colorAttr = {
        node_id: newId,
        attribute_name: "color",
        attribute_value: color,
        holder: false,
      };
      await patchNode(colorAttr);
    } else if (type === "container") {
      const colorAttr = {
        node_id: newId,
        attribute_name: "background",
        attribute_value: color,
        holder: true,
      };
      await patchNode(colorAttr);
      const direction = {
        node_id: newId,
        attribute_name: "direction",
        attribute_value: bgAlign,
        holder: true,
      };
      await patchNode(direction);
    }
  };
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState<FormData | null>(null);
  const [imageUrl, setImageUrl] = useState<string>("");
  const [imageUploaded, setImageUploaded] = useState<boolean>(false);

  const turnEditMode = (
    event: React.MouseEvent<HTMLDivElement, MouseEvent>,
    { id, children, holder, type_id, attrs }: ITreeNode,
  ) => {
    if (event.target === event.currentTarget) {
      setNodeInfo({
        id,
        children,
        holder,
        type_id,
        attrs,
      });
      setActiveItemChoice(id);
      setMenuItems([
        {
          handleClick: () => {
            setNodeInfo(null);
            setActiveItemChoice("");
            setBaseMenu();
          },
          Image: Back,
        },
        {
          handleClick: () => {
            setSelectedType(type_id);
            if (type_id === "container") {
              setBgAlign(attrs.direction as string);
            } else if (type_id === "text") {
              setAlign(attrs.position as string);
              setNodeText(attrs.text as string);
            }
            setOpen(true);
            setBaseMenu();
          },
          Image: Edit,
        },
        {
          handleClick: () => {
            handleDeleteNode(id);
            setBaseMenu();
          },
          Image: Trash,
        },
      ]);
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFormData = new FormData();
      newFormData.append("file", e.target.files[0]);
      setFormData(newFormData);
      setImageUploaded(true);

      const url = URL.createObjectURL(e.target.files[0]);
      setImageUrl(url);
    }
  };
  const [nodeInfo, setNodeInfo] = useState<ITreeNode | null>(null);
  const renderNode = ({
    id,
    children,
    holder,
    type_id,
    attrs,
  }: ITreeNode): React.ReactNode => {
    if (isTreeSuccess && tree && id === tree.id) {
      return children?.map((child) => renderNode(child));
    }

    return (
      <Reorder.Item
        dragListener={id === nodeInfo?.id ? true : false}
        className={`flex-1 w-full ${type_id === "image" ? "h-[30vh]" : "h-full"}`}
        value={id}
        key={id}
      >
        <Drawer>
          <div
            onClick={(event) =>
              turnEditMode(event, { id, children, holder, type_id, attrs })
            }
            style={{
              backgroundSize: "cover",
              backgroundPosition: "50% 75%",
              backgroundColor: type_id === "container" ? attrs.background : "",
              backgroundImage:
                type_id === "image"
                  ? `url(${import.meta.env.VITE_API_URL}:7000/${id})`
                  : "",
            }}
            className={`px-4 py-8 text-4xl gap-4 ${activeItemChoice === id ? "shake" : ""} flex ${attrs?.direction} ${type_id === "image" ? "h-[30vh]" : "h-full"}  w-full h-full border-2 border-black rounded-[15px]`}
          >
            {type_id === "text" && (
              <p
                onClick={(event) =>
                  turnEditMode(event, { id, children, holder, type_id, attrs })
                }
                className={`text-sm break-words relative ${attrs.position} w-full`}
                style={{ color: attrs.color }}
              >
                {attrs.text}
              </p>
            )}
            {children.length > 0 && (
              <Reorder.Group
                axis={attrs.direction === "flex-row" ? "x" : "y"}
                values={children.map((node) => node.id)}
                onReorder={(newOrder: Array<string>) => {
                  console.log(nodeInfo);

                  dispatch(setChildrens({ id: id, children: newOrder }));
                  const newIndex = newOrder.indexOf(nodeInfo!.id);
                  patchNodes({
                    nodeId: nodeInfo!.id,
                    body: { parent: id, position: newIndex },
                  });
                }}
                className={`flex ${attrs.direction} gap-4 w-full ${attrs?.direction === "flex-row" ? "h-[50vh]" : "h-full"} `}
              >
                {children.map((child) => renderNode(child))}
              </Reorder.Group>
            )}
            {holder && children.length < 2 && (
              <DrawerTrigger
                className="w-full h-full"
                onClick={() => {
                  setAnimate(false);
                  setSelectedType(null);
                }}
              >
                <AddButton />
              </DrawerTrigger>
            )}
            {/* !!!!!!!!!!!!!!!!!!!!!! */}
            {/* Drawer For Not Core Node */}
            {/* !!!!!!!!!!!!!!!!!!!!!! */}
            <DrawerContent className="bg-white">
              {selectedType === null && (
                <motion.div
                  key="visible"
                  initial={animate ? { x: "-100%" } : false}
                  animate={{ x: 0 }}
                  exit={{ x: "-100%" }}
                  transition={{ duration: 0.2 }}
                  className="w-full"
                >
                  <DrawerHeader>
                    <DrawerTitle>Выберите шаблон</DrawerTitle>
                  </DrawerHeader>
                  <div className="flex flex-col gap-5 py-5 container">
                    <div
                      onClick={async () => {
                        setAnimate(true);
                        setSelectedType("container");
                      }}
                      className="flex justify-between items-center p-3 rounded-20 border"
                    >
                      <span className="text-2xl font-bold">Блок</span>
                      <div className=" bg-black/50 rounded-20" />
                      <Container className="w-20 h-20" />
                    </div>
                    <div
                      onClick={() => {
                        setAnimate(true);
                        setSelectedType("text");
                      }}
                      className="flex justify-between items-center p-3 rounded-20 border"
                    >
                      <span className="text-2xl font-bold">Текст</span>
                      <Text className="w-20 h-20 stroke-black" />
                    </div>
                    <div
                      onClick={async () => {
                        setAnimate(true);
                        setSelectedType("image");
                      }}
                      className="flex justify-between items-center p-3 rounded-20 border"
                    >
                      <span className="text-2xl font-bold">Изображение</span>
                      <Image className="w-20 h-20" />
                    </div>
                  </div>
                </motion.div>
              )}
              {selectedType === "text" && (
                <motion.div
                  key="hidden"
                  initial={{ x: "100%" }}
                  animate={{ x: 0 }}
                  exit={{ x: "100%" }}
                  transition={{ duration: 0.2 }}
                  // className="absolute bottom-0 bg-white w-full"
                >
                  <DrawerHeader className="flex justify-between items-center">
                    <Return
                      onClick={() => {
                        setAnimate(true);
                        setSelectedType(null);
                      }}
                    />
                    <DrawerTitle className="mx-auto">Текст</DrawerTitle>
                  </DrawerHeader>
                  <form
                    onSubmit={async (e) => {
                      e.preventDefault();
                      const newId = await addNode(id, getIdByType("text"));
                      return await handleSubmit(e, {
                        newId: newId,
                        type: "text",
                      });
                    }}
                    className="flex flex-col gap-5 py-5 container "
                  >
                    <Alignment align={align} setAlign={setAlign} />
                    <InputDefault
                      type="text"
                      name="nodeText"
                      handleChange={setNodeText}
                      valueInp={nodeText}
                      placeholder="Введите текст"
                      className="placeholder:text-mainBlack text-mainBlack"
                    />
                    <input id="color" name="color" type="color" />
                    <DrawerTrigger>
                      <LinkButton
                        title="Сохранить"
                        buttonActive={nodeText === "" ? true : false}
                        type="submit"
                      />
                    </DrawerTrigger>
                  </form>
                </motion.div>
              )}
              {selectedType === "container" && (
                <motion.div
                  key="hidden"
                  initial={{ x: "100%" }}
                  animate={{ x: 0 }}
                  exit={{ x: "100%" }}
                  transition={{ duration: 0.2 }}
                  // className="absolute bottom-0 bg-white w-full"
                >
                  <DrawerHeader className="flex justify-between items-center">
                    <Return
                      onClick={() => {
                        setAnimate(true);
                        setSelectedType(null);
                      }}
                    />
                    <DrawerTitle className="mx-auto">Блок</DrawerTitle>
                  </DrawerHeader>
                  <form
                    onSubmit={async (e) => {
                      e.preventDefault();
                      const newId = await addNode(id, getIdByType("container"));
                      await handleSubmit(e, { newId, type: "container" });
                    }}
                    className="flex flex-col gap-5 py-5 container "
                  >
                    <BgAlignment align={bgAlign} setAlign={setBgAlign} />
                    <input
                      id="color"
                      name="color"
                      type="color"
                      defaultValue={"#ffffff"}
                    />
                    <DrawerTrigger>
                      <LinkButton
                        title="Сохранить"
                        buttonActive={false}
                        type="submit"
                      />
                    </DrawerTrigger>
                  </form>
                </motion.div>
              )}
              {selectedType === "image" && (
                <motion.div
                  key="hidden"
                  initial={{ x: "100%" }}
                  animate={{ x: 0 }}
                  exit={{ x: "100%" }}
                  transition={{ duration: 0.2 }}
                  // className="absolute bottom-0 bg-white w-full"
                >
                  <DrawerHeader className="flex justify-between items-center">
                    <Return
                      onClick={() => {
                        setAnimate(true);
                        setSelectedType(null);
                      }}
                    />
                    <DrawerTitle className="mx-auto">Изображение</DrawerTitle>
                  </DrawerHeader>
                  <form
                    onSubmit={async (e: React.FormEvent<HTMLFormElement>) => {
                      e.preventDefault();
                      if (formData) {
                        const newId = await addCoreNode(
                          id,
                          getIdByType("image"),
                        );
                        formData.append("node_id", newId);
                        await axiosBase.post("images/", formData);
                        queryClient.invalidateQueries("getTreeNodes");
                        setImageUrl("");
                        setImageUploaded(false);
                        setActiveItemChoice("");
                      }
                    }}
                    className="flex flex-col gap-5 py-5 container "
                  >
                    <div className="relative flex justify-center items-center  border-2 border-black w-full rounded-20">
                      <input
                        type="file"
                        onChange={handleImageUpload}
                        className="w-full h-full px-4 py-4 relative z-10  opacity-0"
                      />
                      <Upload className="absolute" />
                    </div>

                    {imageUrl && <img src={imageUrl} alt="Uploaded" />}
                    <DrawerTrigger>
                      <LinkButton
                        title="Сохранить"
                        buttonActive={!imageUploaded}
                        type="submit"
                      />
                    </DrawerTrigger>
                  </form>
                </motion.div>
              )}
            </DrawerContent>
          </div>
        </Drawer>
      </Reorder.Item>
    );
  };

  return (
    <div className=" h-full bg-white">
      {/* !!!!!!!!!!!!!!!!!!!!!! */}
      {/* Drawer for Edit */}
      {/* !!!!!!!!!!!!!!!!!!!!!! */}
      {nodeInfo !== null && (
        <Drawer
          open={open}
          onOpenChange={setOpen}
          onClose={() => {
            setActiveItemChoice("");
            setNodeInfo(null);
          }}
        >
          <DrawerContent className="bg-white">
            {selectedType === "text" && (
              <div>
                <DrawerHeader className="flex justify-between items-center">
                  <DrawerTitle className="mx-auto">Текст</DrawerTitle>
                </DrawerHeader>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault();
                    await handleSubmit(e, {
                      newId: nodeInfo.id,
                      type: "text",
                    });
                    setActiveItemChoice("");
                    setNodeInfo(null);
                    setOpen(false);
                  }}
                  className="flex flex-col gap-5 py-5 container "
                >
                  <Alignment align={align} setAlign={setAlign} />
                  <InputDefault
                    type="text"
                    name="nodeText"
                    handleChange={setNodeText}
                    valueInp={nodeText}
                    placeholder="Введите текст"
                    className="placeholder:text-mainBlack text-mainBlack"
                  />
                  <input
                    id="color"
                    name="color"
                    type="color"
                    defaultValue={nodeInfo.attrs.color}
                  />
                  <LinkButton
                    title="Сохранить"
                    buttonActive={nodeText === "" ? true : false}
                    type="submit"
                  />
                </form>
              </div>
            )}
            {selectedType === "container" && (
              <div>
                <DrawerHeader className="flex justify-between items-center">
                  <DrawerTitle className="mx-auto">Блок</DrawerTitle>
                </DrawerHeader>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault();
                    await handleSubmit(e, {
                      newId: nodeInfo.id,
                      type: "container",
                    });
                    setActiveItemChoice("");
                    setNodeInfo(null);
                    setOpen(false);
                  }}
                  className="flex flex-col gap-5 py-5 container "
                >
                  <BgAlignment align={bgAlign} setAlign={setBgAlign} />
                  <input
                    id="color"
                    name="color"
                    type="color"
                    defaultValue={nodeInfo.attrs.background}
                  />
                  <LinkButton
                    title="Сохранить"
                    buttonActive={false}
                    type="submit"
                  />
                </form>
              </div>
            )}
            {selectedType === "image" && (
              <div>
                <DrawerHeader className="flex justify-between items-center">
                  <DrawerTitle className="mx-auto">Изображение</DrawerTitle>
                </DrawerHeader>
                <form
                  onSubmit={async (e: React.FormEvent<HTMLFormElement>) => {
                    e.preventDefault();
                    if (formData) {
                      formData.append("node_id", nodeInfo.id);
                      await axiosBase.post("images/", formData);
                      queryClient.invalidateQueries("getTreeNodes");
                      setImageUrl("");
                      setImageUploaded(false);
                      setActiveItemChoice("");
                      setNodeInfo(null);
                      setOpen(false);
                    }
                  }}
                  className="flex flex-col gap-5 py-5 container "
                >
                  <div className="relative flex justify-center items-center  border-2 border-black w-full rounded-20">
                    <input
                      type="file"
                      onChange={handleImageUpload}
                      className="w-full h-full px-4 py-4 relative z-10  opacity-0"
                    />
                    <Upload className="absolute" />
                  </div>

                  {imageUrl && <img src={imageUrl} alt="Uploaded" />}
                  <LinkButton
                    title="Сохранить"
                    buttonActive={!imageUploaded}
                    type="submit"
                  />
                </form>
              </div>
            )}
          </DrawerContent>
        </Drawer>
      )}

      {/* !!!!!!!!!!!!!!!!!!!!!! */}
      {/* Drawer for Core Node */}
      {/* !!!!!!!!!!!!!!!!!!!!!! */}
      <Drawer>
        <AnimatePresence mode="popLayout" initial={false}>
          {nodes.children.length > 0 && (
            <Reorder.Group
              values={nodes.children.map((node) => node.id)}
              onReorder={(newOrder: Array<string>) => {
                const newIndex = newOrder.indexOf(nodeInfo!.id);
                patchNodes({
                  nodeId: nodeInfo!.id,
                  body: { parent: nodes.id, position: newIndex },
                });
                dispatch(setChildrens({ id: nodes.id, children: newOrder }));
              }}
              className="h-full grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-5"
            >
              {renderNode(nodes as ITreeNode)}
            </Reorder.Group>
          )}
        </AnimatePresence>
        <DrawerTrigger
          className="w-full h-full"
          onClick={() => {
            setAnimate(false);
            setSelectedType(null);
          }}
        >
          <AddButton className="h-screen" />
        </DrawerTrigger>

        <DrawerContent className="bg-white">
          {selectedType === null && (
            <motion.div
              key="visible"
              initial={animate ? { x: "-100%" } : false}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ duration: 0.2 }}
              className=" w-full"
            >
              <DrawerHeader>
                <DrawerTitle>Выберите шаблон</DrawerTitle>
              </DrawerHeader>
              <div className="flex flex-col gap-5 py-5 container">
                <div
                  onClick={async () => {
                    setAnimate(true);
                    setSelectedType("container");
                  }}
                  className="flex justify-between items-center p-3 rounded-20 border"
                >
                  <span className="text-2xl font-bold">Блок</span>
                  <div className=" bg-black/50 rounded-20" />
                  <Container className="w-20 h-20" />
                </div>
                <div
                  onClick={() => {
                    setAnimate(true);
                    setSelectedType("text");
                  }}
                  className="flex justify-between items-center p-3 rounded-20 border"
                >
                  <span className="text-2xl font-bold">Текст</span>
                  <Text className="w-20 h-20 stroke-black" />
                </div>
                <div
                  onClick={async () => {
                    setAnimate(true);
                    setSelectedType("image");
                  }}
                  className="flex justify-between items-center p-3 rounded-20 border"
                >
                  <span className="text-2xl font-bold">Изображение</span>
                  <Image className="w-20 h-20" />
                </div>
              </div>
            </motion.div>
          )}
          {selectedType === "text" && (
            <motion.div
              key="hidden"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ duration: 0.2 }}
              // className="absolute bottom-0 bg-white w-full"
            >
              <DrawerHeader className="flex justify-between items-center">
                <Return
                  onClick={() => {
                    setAnimate(true);
                    setSelectedType(null);
                  }}
                />
                <DrawerTitle className="mx-auto">Текст</DrawerTitle>
              </DrawerHeader>
              <form
                onSubmit={async (e) => {
                  e.preventDefault();
                  const newId = await addCoreNode(
                    tree ? tree.id : "",
                    getIdByType("text"),
                  );
                  await handleSubmit(e, { newId, type: "text" });
                }}
                className="flex flex-col gap-5 py-5 container "
              >
                <Alignment align={align} setAlign={setAlign} />
                <InputDefault
                  type="text"
                  name="nodeText"
                  handleChange={setNodeText}
                  valueInp={nodeText}
                  placeholder="Введите текст"
                  className="placeholder:text-mainBlack text-mainBlack"
                />
                <input id="color" name="color" type="color" />
                <DrawerTrigger>
                  <LinkButton
                    title="Сохранить"
                    buttonActive={nodeText === "" ? true : false}
                    type="submit"
                  />
                </DrawerTrigger>
              </form>
            </motion.div>
          )}
          {selectedType === "container" && (
            <motion.div
              key="hidden"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ duration: 0.2 }}
              // className="absolute bottom-0 bg-white w-full"
            >
              <DrawerHeader className="flex justify-between items-center">
                <Return
                  onClick={() => {
                    setAnimate(true);
                    setSelectedType(null);
                  }}
                />
                <DrawerTitle className="mx-auto">Блок</DrawerTitle>
              </DrawerHeader>
              <form
                onSubmit={async (e) => {
                  e.preventDefault();
                  const newId = await addCoreNode(
                    tree ? tree.id : "",
                    getIdByType("container"),
                  );
                  await handleSubmit(e, { newId, type: "container" });
                }}
                className="flex flex-col gap-5 py-5 container "
              >
                <BgAlignment align={bgAlign} setAlign={setBgAlign} />
                <input
                  id="color"
                  name="color"
                  type="color"
                  defaultValue={"#ffffff"}
                />
                <DrawerTrigger>
                  <LinkButton
                    title="Сохранить"
                    buttonActive={false}
                    type="submit"
                  />
                </DrawerTrigger>
              </form>
            </motion.div>
          )}
          {selectedType === "image" && (
            <motion.div
              key="hidden"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ duration: 0.2 }}
              // className="absolute bottom-0 bg-white w-full"
            >
              <DrawerHeader className="flex justify-between items-center">
                <Return
                  onClick={() => {
                    setAnimate(true);
                    setSelectedType(null);
                  }}
                />
                <DrawerTitle className="mx-auto">Изображение</DrawerTitle>
              </DrawerHeader>
              <form
                onSubmit={async (e: React.FormEvent<HTMLFormElement>) => {
                  e.preventDefault();
                  if (formData) {
                    const newId = await addNode(
                      tree ? tree.id : "",
                      getIdByType("image"),
                    );
                    formData.append("node_id", newId);
                    await axiosBase.post("images/", formData);
                    queryClient.invalidateQueries("getTreeNodes");
                    setImageUrl("");
                    setImageUploaded(false);
                    setActiveItemChoice("");
                  }
                }}
                className="flex flex-col gap-5 py-5 container "
              >
                <div className="relative flex justify-center items-center  border-2 border-black w-full rounded-20">
                  <input
                    type="file"
                    onChange={handleImageUpload}
                    className="w-full h-full px-4 py-4 relative z-10  opacity-0"
                  />
                  <Upload className="absolute" />
                </div>

                {imageUrl && <img src={imageUrl} alt="Uploaded" />}
                <DrawerTrigger>
                  <LinkButton
                    title="Сохранить"
                    buttonActive={!imageUploaded}
                    type="submit"
                  />
                </DrawerTrigger>
              </form>
            </motion.div>
          )}
        </DrawerContent>
      </Drawer>
    </div>
  );
};

export default UserPage;
