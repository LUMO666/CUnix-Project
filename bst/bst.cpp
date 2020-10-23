#include <iostream>
using namespace std;

#define list_entry(ptr, type, member) \
        container_of(ptr, type, member)
#define container_of(ptr, type, member) ({                  \
        const typeof(((type *)0)->member) *__mptr= (ptr);  \
        (type *)( (char *)__mptr - offsetof(type,member) );})
#define offsetof(type, member) \
        ((size_t) &((type *)0)->member)

struct branch{
    struct branch* lc;
    struct branch* rc;
    branch():lc(NULL), rc(NULL){}
};

//struct node *n =list_entry(pointer, struct node, list);
//printf("%d\n", n->data);

struct node 
{
    int data;
    struct branch list;
    node():data(0), list(){}
};


// bst
class bstree
{
public:
    enum
    {
        hmax_size_32767     = 32767,
        hmin_size_0         = 0,
    };

public:

    // 构造函数
    bstree()
        : root(NULL)
        , size(0)
    {
    }

    // 析构函数
    virtual ~bstree(){}
    
    int get_size()
    {
        return size;
    }

    // 插入结点
    void insert_node(int data)
    {
        int cur_size = get_size();
        if (hmax_size_32767 == cur_size)
        {
            cout << "insert node error, the size of the tree is max" << endl;
            return ;
        }
        root = insert(root, data);
    }

    // 先序遍历（前序遍历）
    void pre_order()
    {
        pre_order_traverse(root);
    }

    // 中序遍历
    void in_order()
    {
        in_order_traverse(root);
    }

    // 后序遍历
    void post_order()
    {
        post_order_traverse(root);
    }

    /*
        查找某个结点
        int key - 查找结果

        返回值：
            NULL : 可能为root为空 或者 没有找到
            != NULL, 找到结点
    */
    branch* query(int key)
    {
        if (NULL == root)
        {
            cout << "query error, root = null" << endl;
            return NULL;
        }

        return query_node(root, key);
    }

    // 删除树
    void remove_all()
    {
        if (NULL == root)
        {
            cout << "remove all failed, root = null" << endl;
            return;
        }
        
        remove_all(root);

        int cur_size = get_size();
        if (0 == cur_size)
            root = NULL;
    }

    // 删除某个结点
    void remove_node(int del_data)
    {
        if (NULL == root)
        {
            cout << "remove node error, root = null" << endl;
            return;
        }

        branch *parent_node   = NULL;
        branch *del_node      = root;

        
        // 找到删除结点的父节点与删除结点
        while (del_node)
        {
            struct node *ddata = list_entry(del_node, struct node, list);
            if (del_data == ddata->data)
                break;
            else if (del_data > ddata->data)
            {
                parent_node = del_node;
                del_node    = del_node->rc;
            }
            else if (del_data < ddata->data)
            {
                parent_node = del_node;
                del_node = del_node->lc;
            }
        }

        // 若没有找到要删除的结点
        if (NULL == del_node)
        {
            cout << "remove node error, " << del_data << " was not find" << endl;
            return;
        }

        // 1、若删除的结点没有左子树和右子树
        if ( (NULL == del_node->lc) && (NULL == del_node->rc)  )
        {
            // 为什么要先判断根结点，因为根结点的父节点找不到，结果为NULL，
            // 1.1 可能只有一个根结点， 将root释放值为空
            if (del_node == root)
            {
                root = NULL;
                struct node *dnode = list_entry(del_node, struct node, list);
                delete dnode;
                del_node = NULL;

                dec_size();
                return;
            }

            // 1.2 非根结点，那就是叶子结点了， 将父节点指向删除结点的分支指向NULL
            if  (del_node == parent_node->lc)
                parent_node->lc = NULL;
            else if (del_node == parent_node->rc)
                parent_node->rc  = NULL;

            // 释放结点
            struct node *dnode = list_entry(del_node, struct node, list);
            delete dnode;
            del_node = NULL;
            dec_size();
        }

        // 2、若删除结点只有左孩子，没有右孩子
        else if ( (NULL != del_node->lc) && (NULL == del_node->rc) )
        {
            // 2.1 删除结点为根结点，则将删除结点的左孩子替代当前删除结点
            if (del_node == root)
            {
                root = root->lc;
            }
            // 2.2 其他结点，将删除结点的左孩子作为父节点的左孩子
            else
            {
                if (parent_node->lc == del_node)
                    parent_node->lc = del_node->lc;
                else if (parent_node->rc == del_node)
                    parent_node->rc = del_node->lc;
            }
            struct node *dnode = list_entry(del_node, struct node, list);
            delete dnode;
            del_node = NULL;

            dec_size();
        }

        // 3、若删除结点只有右孩子
        else if ( (NULL == del_node->lc) && (NULL != del_node->rc) )
        {
            // 3.1 若为根结点
            if (root == del_node)
            {
                root = root->rc;
            }
            else
            {
                if (del_node == parent_node->lc)
                    parent_node->lc = del_node->rc;
                else if (del_node == parent_node->rc)
                    parent_node->rc = del_node->rc;
            }
            struct node *dnode = list_entry(del_node, struct node, list);
            delete dnode;
            del_node = NULL;

            dec_size();
        }

        // 4、若删除结点既有左孩子，又有右孩子,需要找到删除结点的后继结点作为根结点
        else if ( (NULL != del_node->lc) && (NULL != del_node->rc) )
        {
            branch *successor_node = del_node->rc;
            parent_node = del_node;

            while (successor_node->lc)
            {
                parent_node = successor_node;
                successor_node = successor_node->lc;
            }

            // 交换后继结点与当前删除结点的数据域
            struct node *ddata = list_entry(del_node, struct node, list);
            struct node *sdata = list_entry(successor_node, struct node, list);
            ddata->data = sdata->data;
            // 将指向后继结点的父节点的孩子设置后继结点的右子树
            if (successor_node == parent_node->lc)
                parent_node->lc = successor_node->rc;
            else if (successor_node == parent_node->rc)
                parent_node->rc = successor_node->rc;

            // 删除后继结点
            del_node = successor_node;
            struct node *dnode = list_entry(del_node, struct node, list);
            delete dnode;
            del_node = NULL;

            dec_size();
        }
    }

    // 返回以proot为根结点的最小结点
    branch *get_min_node(branch *proot)
    {
        if (NULL == proot->lc)
            return proot;

        return get_min_node(proot->lc);
    }

    // 返回以proo为根节点的最大结点
    branch *get_max_node(branch *proot)
    {
        if (NULL == proot->rc)
            return proot;
        
        return get_max_node(proot->rc);
    }

    // 返回根节点
    branch *get_root_node()
    {
        return root;
    }

    // 返回proot结点的父节点
    branch *get_parent_node(int key)
    {
        // 当前结点
        branch *cur_node = NULL;
        // 父节点
        branch *parent_node = NULL;

        cur_node = root;

        // 标记是否找到
        bool is_find = false;
        while (cur_node)
        {
            struct node *cdata = list_entry(cur_node, struct node, list);
            if (key == cdata->data)
            {
                is_find = true;
                break;
            }

            // 因为比当前结点的值还要小，所以需要查找当前结点的左子树
            else if (key < cdata->data)
            {
                parent_node = cur_node;
                cur_node = cur_node->lc;
            }
            // 同上， 查找当前结点的右子树
            else if (key > cdata->data)
            {
                parent_node = cur_node;
                cur_node    = cur_node->rc;
            }
        }

        return (true == is_find)?  parent_node :  NULL; 
    }

   






private:


    //查找某个值
    branch *query_node(branch *proot, int key)
    {
        if (NULL == proot)
        {
            return proot;
        }
        struct node *pdata = list_entry(proot, struct node, list);
        if (pdata->data == key)
            return proot;
        else if (pdata->data > key)
        {
            return query_node(proot->lc, key);
        }
        else if (pdata->data < key)
        {
            return query_node(proot->rc, key);
        }
        
        return NULL;
    }

    // 后序遍历删除所有结点
    void remove_all(branch *proot)
    {
        if (NULL != proot)
        {            
            remove_all(proot->lc);
            remove_all(proot->rc);
            struct node *dnode = list_entry(proot, struct node, list);
            delete dnode;

            dec_size();
        }
    }

    // 先序遍历
    void pre_order_traverse(branch *proot)
    {
        if (NULL != proot)
        {
            struct node *pdata = list_entry(proot, struct node, list);
            cout << pdata->data << ",   "; 
            pre_order_traverse(proot->lc);
            pre_order_traverse(proot->rc);
        }
    }

    // 中序遍历
    void in_order_traverse(branch *proot)
    {
        if (NULL != proot)
        {
            struct node *pdata = list_entry(proot, struct node, list);
            in_order_traverse(proot->lc);
            cout << pdata->data << ",   "; 
            in_order_traverse(proot->rc);
        }
    }

    // 后续遍历
    void post_order_traverse(branch *proot)
    {
        if (NULL != proot)
        {
            struct node *pdata = list_entry(proot, struct node, list);
            post_order_traverse(proot->lc);
            post_order_traverse(proot->rc);
            cout << pdata->data << ",   ";
        }
    }

    // 插入结点
    branch* insert(branch* proot, int data)
    {
        struct node *pdata = list_entry(proot, struct node, list);
        // 结点不存在， 则创建
        if (NULL == proot)
        {
            struct node *new_node = new(std::nothrow) node;
            if (NULL != new_node)
            {
                new_node->data = data;
                proot = &(new_node->list);
                
                // 结点+1；
                add_size();
            }

            return proot;
        }

        //  插入值比当前结点值还要小， 则应该插入到当前节点的左边
        if (pdata->data > data)
        {
            proot->lc = insert(proot->lc, data);
        }
        // 插入之比当前结点值还要打，则应该插入到当前结点的右边
        else if (pdata->data < data)
        {
            proot->rc = insert(proot->rc, data);
        }

        // 相等，则不插入结点。

        return proot;
    }

    // size + 1
    void add_size()
    {
        if (hmax_size_32767 == size)
            return ;
        size++;
    }

    // size - 1
    void dec_size()
    {
        if ( hmin_size_0 == size)
        {
            return ;
        }

        size--;
    }




private:
    // 根结点
    branch *root;

    // 当前树的结点个数
    int size;
};



// 测试代码
int main()
{

    bstree tree;

    //
    tree.insert_node(50);

    tree.insert_node(30);
    tree.insert_node(10);
    tree.insert_node(0);
    tree.insert_node(20);
    tree.insert_node(40);

    tree.insert_node(70);
    tree.insert_node(90);
    tree.insert_node(100);
    tree.insert_node(60);
    tree.insert_node(80);

    // 前序遍历
    cout << "前序遍历" << endl;
    tree.pre_order();
    cout << endl;

    // 中序遍历
    cout << "中序遍历" << endl;
    tree.in_order();
    cout << endl;

    // 后序遍历
    cout << "后序遍历" << endl;
    tree.post_order();
    cout << endl;

    cout << "删除结点开始，结束请输入10086" << endl;

    int del_key = 0;

    while (true)
    {
        cout << "输入删除结点值 = ";
        cin >> del_key;
        if (10086 == del_key)
            break;

        tree.remove_node(del_key);

        cout << "删除后,结点个数 = " << tree.get_size() << endl;
        cout << "删除后， 中序遍历结果:" ;// << endl;
        tree.in_order();
        cout << endl << endl;
    }

    tree.remove_all();

    return 0;
}